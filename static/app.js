// Local storage keys
const STORAGE_KEY_COURSES = "ai_learning_assistant_courses";

// Application State
let appState = {
    courses: [],
    activeCourseIndex: null
};

// Markdown to HTML simple parser
function parseMarkdown(md) {
    if (!md) return "";
    let html = md;
    
    // Headings
    html = html.replace(/^##\s+(.*)$/gm, '<h3 style="color: #ffffff; margin-top: 1.5rem; margin-bottom: 0.75rem; font-weight: 700; font-size: 1.35rem;">$1</h3>');
    html = html.replace(/^###\s+(.*)$/gm, '<h4 style="color: #a78bfa; margin-top: 1.25rem; margin-bottom: 0.5rem; font-weight: 600; font-size: 1.15rem;">$1</h4>');
    
    // Bold text
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #ffffff; font-weight: 700;">$1</strong>');
    
    // Inline code
    html = html.replace(/`(.*?)`/g, '<code style="background: rgba(0,0,0,0.3); padding: 0.2rem 0.4rem; border-radius: 6px; font-family: monospace; font-size: 0.9rem; color: #ec4899;">$1</code>');
    
    // Bullet points
    html = html.replace(/^\s*[-*]\s+(.*)$/gm, '<li style="margin-left: 20px; color: #cbd5e1; margin-bottom: 5px;">$1</li>');
    
    // Numbered items
    html = html.replace(/^\s*(\d+)\.\s+(.*)$/gm, '<li style="margin-left: 20px; color: #cbd5e1; margin-bottom: 5px; list-style-type: decimal;">$2</li>');
    
    // Line breaks
    html = html.replace(/\n/g, '<br>');
    
    return html;
}

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
    loadCoursesFromStorage();
    renderDashboard();
    setupEventListeners();
});

// Load courses from Local Storage
function loadCoursesFromStorage() {
    const raw = localStorage.getItem(STORAGE_KEY_COURSES);
    if (raw) {
        try {
            appState.courses = JSON.parse(raw);
        } catch (e) {
            console.error("Error parsing courses from storage:", e);
            appState.courses = [];
        }
    } else {
        appState.courses = [];
    }
}

// Save courses to Local Storage
function saveCoursesToStorage() {
    localStorage.setItem(STORAGE_KEY_COURSES, JSON.stringify(appState.courses));
}

// DOM Elements
const dashboardView = document.getElementById("dashboard-view");
const courseView = document.getElementById("course-view");
const loadingOverlay = document.getElementById("loading-overlay");
const loadingOverlayText = document.getElementById("loading-overlay-text");

// Render Dashboard
function renderDashboard() {
    // 1. Render Stats
    let totalCourses = appState.courses.length;
    let completedCheckpoints = 0;
    let totalScoreSum = 0;
    let gradedCount = 0;
    
    appState.courses.forEach(c => {
        completedCheckpoints += c.checkpoint_idx;
        c.states.forEach(s => {
            if (s && s.understanding_score > 0) {
                totalScoreSum += s.understanding_score;
                gradedCount++;
            }
        });
    });
    
    const avgScore = gradedCount > 0 ? Math.round(totalScoreSum / gradedCount) : 0;
    
    document.getElementById("stats-active-courses").innerText = totalCourses;
    document.getElementById("stats-checkpoints").innerText = completedCheckpoints;
    document.getElementById("stats-avg-score").innerText = `${avgScore}%`;
    
    // 2. Render Courses List
    const historyList = document.getElementById("courses-history-list");
    historyList.innerHTML = "";
    
    if (appState.courses.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-graduation-cap"></i>
                <p>No active courses yet. Enter a topic above to begin!</p>
            </div>
        `;
        return;
    }
    
    appState.courses.forEach((course, index) => {
        const completedPercent = Math.round((course.checkpoint_idx / 5) * 100);
        
        const item = document.createElement("div");
        item.className = "course-item";
        item.innerHTML = `
            <div class="course-info">
                <div class="course-name">${course.topic}</div>
                <div class="course-progress-container">
                    <div class="course-progress-mini-bar">
                        <div class="course-progress-mini-fill" style="width: ${completedPercent}%;"></div>
                    </div>
                    <div class="course-progress-text">${course.checkpoint_idx}/5 checkpoints</div>
                </div>
            </div>
            <div class="course-actions">
                <button class="btn-resume" data-index="${index}"><i class="fas fa-play"></i> Resume</button>
                <button class="btn-delete" data-index="${index}"><i class="fas fa-trash-alt"></i></button>
            </div>
        `;
        historyList.appendChild(item);
    });
}

// Show & Hide Loader
function showLoader(message = "AI is working...") {
    loadingOverlayText.innerText = message;
    loadingOverlay.classList.remove("hidden");
}

function hideLoader() {
    loadingOverlay.classList.add("hidden");
}

// Navigate Views
function showView(viewName) {
    if (viewName === "dashboard") {
        dashboardView.classList.remove("hidden");
        courseView.classList.add("hidden");
        renderDashboard();
    } else {
        dashboardView.classList.add("hidden");
        courseView.classList.remove("remove", "hidden");
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Back to Dashboard
    document.getElementById("btn-back-to-dashboard").addEventListener("click", () => {
        appState.activeCourseIndex = null;
        showView("dashboard");
    });
    
    // Generate Path
    document.getElementById("new-course-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const topic = document.getElementById("course-topic").value.trim();
        if (!topic) return;
        
        showLoader("🤖 AI is designing your progressive learning roadmap...");
        
        try {
            const res = await fetch("/api/checkpoints", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic })
            });
            
            const checkpoints = await res.json();
            if (checkpoints && checkpoints.length > 0) {
                // Add new course to state
                const newCourse = {
                    topic: topic,
                    checkpoints: checkpoints,
                    checkpoint_idx: 0,
                    states: [null, null, null, null, null] // holds graph state for each of the 5 checkpoints
                };
                
                appState.courses.unshift(newCourse); // Add to beginning
                appState.activeCourseIndex = 0;
                saveCoursesToStorage();
                
                // Clear input
                document.getElementById("course-topic").value = "";
                
                // Load checkpoint 1
                await loadCheckpoint(0);
            } else {
                alert("Failed to generate checkpoints. Please try another topic.");
            }
        } catch (err) {
            console.error("Error creating path:", err);
            alert("Error connecting to server. Please try again.");
        } finally {
            hideLoader();
        }
    });
    
    // Resume & Delete Buttons Click Handler (Delegated)
    document.getElementById("courses-history-list").addEventListener("click", async (e) => {
        const resumeBtn = e.target.closest(".btn-resume");
        const deleteBtn = e.target.closest(".btn-delete");
        
        if (resumeBtn) {
            const index = parseInt(resumeBtn.dataset.index);
            appState.activeCourseIndex = index;
            const course = appState.courses[index];
            
            // If already complete, go to complete state or load checkpoint
            if (course.checkpoint_idx >= 5) {
                loadCheckpoint(4); // Load last checkpoint
            } else {
                await loadCheckpoint(course.checkpoint_idx);
            }
        }
        
        if (deleteBtn) {
            const index = parseInt(deleteBtn.dataset.index);
            if (confirm(`Are you sure you want to delete "${appState.courses[index].topic}"?`)) {
                appState.courses.splice(index, 1);
                saveCoursesToStorage();
                renderDashboard();
            }
        }
    });
    
    // Toggle Study Material expander
    document.getElementById("study-material-header").addEventListener("click", () => {
        const body = document.getElementById("study-material-body");
        const icon = document.querySelector("#toggle-study-material i");
        body.classList.toggle("collapsed");
        icon.classList.toggle("rotated");
    });
    
    // Submit MCQ Quiz Form
    document.getElementById("quiz-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const activeIdx = appState.activeCourseIndex;
        const course = appState.courses[activeIdx];
        const cpIdx = course.checkpoint_idx;
        let graphState = course.states[cpIdx];
        
        // Retrieve choices
        const userAnswers = [];
        const questionBlocks = document.querySelectorAll(".quiz-question-box");
        let answeredAll = true;
        
        questionBlocks.forEach((block, qIdx) => {
            const selectedOption = block.querySelector(".option-card.selected");
            if (selectedOption) {
                userAnswers.push(`${qIdx + 1}.${selectedOption.dataset.letter}`);
            } else {
                answeredAll = false;
            }
        });
        
        if (!answeredAll) {
            alert("Please answer all 5 questions before submitting!");
            return;
        }
        
        showLoader("📝 Submitting answers to AI Teacher for grading...");
        
        // Update state on backend
        graphState.learner_answers = userAnswers.join(", ");
        
        try {
            const res = await fetch("/api/invoke", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(graphState)
            });
            
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || "Server error");
            }
            
            const updatedState = await res.json();
            course.states[cpIdx] = updatedState;
            saveCoursesToStorage();
            
            // Re-render
            renderCourseView();
        } catch (err) {
            console.error("Error grading answers:", err);
            alert("Error connecting to server. Please try again.");
        } finally {
            hideLoader();
        }
    });
    
    // Feynman Retake Assessment Click
    document.getElementById("btn-retake-quiz").addEventListener("click", async () => {
        const activeIdx = appState.activeCourseIndex;
        const course = appState.courses[activeIdx];
        const cpIdx = course.checkpoint_idx;
        let graphState = course.states[cpIdx];
        
        showLoader("🔄 Re-generating questions...");
        
        // Reset properties
        graphState.questions = [];
        graphState.learner_answers = "";
        graphState.understanding_score = 0;
        graphState.feedback = "";
        
        try {
            const res = await fetch("/api/invoke", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(graphState)
            });
            
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || "Server error");
            }
            
            const updatedState = await res.json();
            course.states[cpIdx] = updatedState;
            saveCoursesToStorage();
            
            renderCourseView();
        } catch (err) {
            console.error("Error retaking quiz:", err);
            alert("Error connecting to server.");
        } finally {
            hideLoader();
        }
    });
    
    // Proceed to Next Checkpoint
    document.getElementById("btn-next-checkpoint").addEventListener("click", async () => {
        const activeIdx = appState.activeCourseIndex;
        const course = appState.courses[activeIdx];
        
        // If course is already completed, just return to dashboard
        if (course.checkpoint_idx >= 5) {
            appState.activeCourseIndex = null;
            showView("dashboard");
            return;
        }
        
        const nextIdx = course.checkpoint_idx + 1;
        
        course.checkpoint_idx = nextIdx;
        saveCoursesToStorage();
        
        if (nextIdx >= 5) {
            // Whole course completed!
            alert("🎉 Congratulations! You have completed all 5 checkpoints and mastered this topic!");
            appState.activeCourseIndex = null;
            showView("dashboard");
        } else {
            showLoader("📚 Loading Next Checkpoint...");
            await loadCheckpoint(nextIdx);
            hideLoader();
        }
    });
}

// Load Checkpoint
async function loadCheckpoint(cpIdx) {
    const activeIdx = appState.activeCourseIndex;
    const course = appState.courses[activeIdx];
    
    // Check if checkpoint state already exists and is valid (not an error object)
    if (!course.states[cpIdx] || course.states[cpIdx].detail) {
        showLoader("📚 AI is compiling your study guide and assessment...");
        
        const initialInput = {
            topic: course.checkpoints[cpIdx].topic,
            objectives: course.checkpoints[cpIdx].obj,
            gathered_context: "",
            relevance_score: 0,
            questions: [],
            learner_answers: "",
            understanding_score: 0,
            search_retry_count: 0,
            feedback: ""
        };
        
        try {
            const res = await fetch("/api/invoke", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(initialInput)
            });
            
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || "Server error");
            }
            
            const stateResult = await res.json();
            course.states[cpIdx] = stateResult;
            saveCoursesToStorage();
        } catch (err) {
            console.error("Error invoking graph for checkpoint load:", err);
            alert("Failed to load checkpoint. Try again.");
            hideLoader();
            return;
        }
    }
    
    renderCourseView();
    showView("course");
    hideLoader();
}

// Render Active Course View
function renderCourseView() {
    const activeIdx = appState.activeCourseIndex;
    const course = appState.courses[activeIdx];
    // Prevent out-of-bounds index if course is completed
    const cpIdx = Math.min(course.checkpoint_idx, 4);
    
    // 1. Set titles
    document.getElementById("active-course-title").innerText = course.topic;
    document.getElementById("current-checkpoint-title").innerText = `Checkpoint ${cpIdx + 1}: ${course.checkpoints[cpIdx].topic}`;
    document.getElementById("current-checkpoint-objectives").innerText = course.checkpoints[cpIdx].obj;
    document.getElementById("course-progress-percent").innerText = `Progress: ${course.checkpoint_idx}/5 completed`;
    
    const progressFillPercent = (course.checkpoint_idx / 5) * 100;
    document.getElementById("course-progress-fill").style.width = `${progressFillPercent}%`;
    
    // 2. Render Sidebar Roadmap
    const roadmapList = document.getElementById("sidebar-roadmap-list");
    roadmapList.innerHTML = "";
    
    course.checkpoints.forEach((cp, index) => {
        let statusClass = "locked";
        let statusIcon = '<i class="fas fa-lock"></i>';
        
        if (index < course.checkpoint_idx) {
            statusClass = "completed";
            statusIcon = '<i class="fas fa-check"></i>';
        } else if (index === course.checkpoint_idx) {
            statusClass = "active";
            statusIcon = '<i class="fas fa-dot-circle"></i>';
        }
        
        const item = document.createElement("div");
        item.className = `roadmap-item ${statusClass}`;
        item.innerHTML = `
            <div class="roadmap-icon">${statusIcon}</div>
            <div class="roadmap-info">
                <div class="roadmap-step">Step ${index + 1}</div>
                <div class="roadmap-title">${cp.topic}</div>
            </div>
        `;
        roadmapList.appendChild(item);
    });
    
    // Get graph state for active checkpoint
    const graphState = course.states[cpIdx];
    
    // 3. Render Study Material
    const studyBody = document.getElementById("study-material-body");
    studyBody.innerHTML = parseMarkdown(graphState.gathered_context);
    
    // Reset Chevron Expander view
    studyBody.classList.remove("collapsed");
    document.querySelector("#toggle-study-material i").classList.remove("rotated");
    
    // 4. Determine phase and render cards
    const questions = graphState.questions || [];
    const rawQ = questions.length > 0 ? String(questions[0]) : "";
    const isFeynman = rawQ.includes("FEYNMAN_PHASE|");
    const score = graphState.understanding_score || 0;
    const feedback = graphState.feedback || "";
    const hasFeedback = feedback.trim() !== "";
    
    const quizCard = document.getElementById("quiz-section-container");
    const feynmanCard = document.getElementById("feynman-section-container");
    const successCard = document.getElementById("success-section-container");
    const feedbackCard = document.getElementById("feedback-section-container");
    
    // Hide all first
    quizCard.classList.add("hidden");
    feynmanCard.classList.add("hidden");
    successCard.classList.add("hidden");
    if (feedbackCard) feedbackCard.classList.add("hidden");
    
    if (score >= 70 && !isFeynman) {
        // SUCCESS CARD
        successCard.classList.remove("hidden");
        document.getElementById("success-score-text").innerHTML = `🎉 Excellent job! You scored <strong>${score}%</strong> and mastered this checkpoint!`;
        
        // Update the next button text based on completion status
        const btnNextText = document.querySelector("#btn-next-checkpoint .btn-text");
        if (course.checkpoint_idx >= 5) {
            btnNextText.innerHTML = "Back to Dashboard <i class='fas fa-home'></i>";
        } else if (cpIdx === 4) {
            btnNextText.innerHTML = "Finish Course <i class='fas fa-flag-checkered'></i>";
        } else {
            btnNextText.innerHTML = "Proceed to Next Checkpoint <i class='fas fa-arrow-right'></i>";
        }
        
        if (hasFeedback && feedbackCard && score < 100) {
            feedbackCard.classList.remove("hidden");
            document.getElementById("feedback-content").innerHTML = parseMarkdown(feedback);
        }
    } else if (isFeynman) {
        // FEYNMAN ADAPTIVE CARD
        feynmanCard.classList.remove("hidden");
        document.getElementById("feynman-score-alert").innerHTML = `<i class="fas fa-exclamation-triangle"></i> You scored <strong>${score}%</strong> — Below mastery threshold (70%). Let's fill the gaps!`;
        
        const explanation = rawQ.replace("FEYNMAN_PHASE|", "");
        document.getElementById("feynman-explanation-box").innerHTML = parseMarkdown(explanation);
        
        if (hasFeedback && feedbackCard) {
            feedbackCard.classList.remove("hidden");
            document.getElementById("feedback-content").innerHTML = parseMarkdown(feedback);
        }
    } else {
        // QUIZ/ASSESSMENT CARD
        quizCard.classList.remove("hidden");
        renderQuizQuestions(rawQ);
    }
}

// Render Quiz Questions inside Form
function renderQuizQuestions(quizText) {
    const list = document.getElementById("quiz-questions-list");
    list.innerHTML = "";
    
    if (!quizText) {
        list.innerHTML = `<div class="empty-state"><i class="fas fa-spinner fa-spin"></i> Preparing assessment questions...</div>`;
        return;
    }
    
    // Split by question number (e.g. 1. or 2.)
    const questionBlocks = quizText.trim().split(/\n(?=\d+\.)/);
    
    questionBlocks.slice(0, 5).forEach((block, qIdx) => {
        if (!block.trim()) return;
        
        const lines = block.trim().split('\n');
        const questionTitle = lines[0].replace(/^\d+\.\s*/, "").trim();
        
        const blockDiv = document.createElement("div");
        blockDiv.className = "quiz-question-box";
        blockDiv.innerHTML = `<div class="question-text"><strong>Q${qIdx + 1}:</strong> ${questionTitle}</div>`;
        
        const optionsGrid = document.createElement("div");
        optionsGrid.className = "options-grid";
        
        lines.slice(1).forEach(line => {
            const lineClean = line.trim();
            // Match A) Option or A. Option
            const match = lineClean.match(/^([A-D])[\).:\s]\s*(.*)/i);
            if (match) {
                const letter = match[1].toUpperCase();
                const optionText = match[2];
                
                const optionCard = document.createElement("div");
                optionCard.className = "option-card";
                optionCard.dataset.letter = letter;
                optionCard.innerHTML = `
                    <div class="option-radio"><div class="option-radio-dot"></div></div>
                    <div class="option-text"><strong>${letter})</strong> ${optionText}</div>
                `;
                
                // Click option handler
                optionCard.addEventListener("click", () => {
                    // Remove selected from other siblings
                    optionsGrid.querySelectorAll(".option-card").forEach(c => c.classList.remove("selected"));
                    optionCard.classList.add("selected");
                });
                
                optionsGrid.appendChild(optionCard);
            }
        });
        
        blockDiv.appendChild(optionsGrid);
        list.appendChild(blockDiv);
    });
}
