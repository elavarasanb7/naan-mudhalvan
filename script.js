// API Configuration
const API_URL = 'http://localhost:5000/api';

// Knowledge base for supply chain management
const knowledgeBase = {
    inventory: {
        keywords: ['inventory', 'stock', 'storage', 'warehouse'],
        responses: [
            "Based on current inventory levels, I recommend optimizing stock levels to reduce holding costs while maintaining service levels.",
            "Our warehouse management system shows real-time inventory tracking and automated reordering capabilities.",
            "I can help you implement ABC analysis for better inventory control and management.",
            "Let's analyze your inventory turnover ratio to identify slow-moving items and optimize storage space.",
            "I can help set up automated reorder points based on lead times and demand patterns."
        ]
    },
    logistics: {
        keywords: ['shipping', 'transport', 'delivery', 'logistics', 'route', 'distribution'],
        responses: [
            "Our logistics network optimization suggests using multi-modal transportation to reduce costs and delivery times.",
            "I can help track shipments and provide real-time updates on delivery status.",
            "Based on current data, I recommend optimizing delivery routes to improve efficiency.",
            "Let's analyze your last-mile delivery performance and identify areas for improvement.",
            "I can help implement cross-docking strategies to reduce warehouse handling time."
        ]
    },
    procurement: {
        keywords: ['supplier', 'vendor', 'purchase', 'procurement', 'buy', 'sourcing'],
        responses: [
            "I can help evaluate supplier performance metrics and suggest improvements.",
            "Our system shows multiple vendor options for your requirements with comparative analysis.",
            "Based on market analysis, now is an optimal time to negotiate new supplier contracts.",
            "Let's implement a strategic sourcing approach to diversify your supplier base.",
            "I can help develop a vendor rating system based on quality, delivery, and cost metrics."
        ]
    },
    forecasting: {
        keywords: ['forecast', 'demand', 'predict', 'planning', 'projection'],
        responses: [
            "Using historical data and market trends, I predict a 15% increase in demand for next quarter.",
            "I can help create a demand forecast using multiple forecasting methods for better accuracy.",
            "Our predictive analytics suggest adjusting safety stock levels for seasonal variations.",
            "Let's implement machine learning models for more accurate demand predictions.",
            "I can help analyze external factors affecting demand patterns in your market."
        ]
    },
    quality_control: {
        keywords: ['quality', 'inspection', 'standards', 'compliance', 'testing', 'defect'],
        responses: [
            "I can help implement a comprehensive quality management system across your supply chain.",
            "Let's set up automated quality inspection checkpoints at key stages of the process.",
            "Based on recent data, I recommend implementing Six Sigma methodologies to reduce defects.",
            "Our analysis shows opportunities to improve supplier quality compliance.",
            "I can help develop quality metrics and KPIs for better monitoring and control."
        ]
    },
    sustainability: {
        keywords: ['sustainable', 'green', 'environmental', 'carbon', 'recycling', 'emissions'],
        responses: [
            "Let's analyze your supply chain's carbon footprint and identify reduction opportunities.",
            "I can help implement sustainable packaging solutions to reduce environmental impact.",
            "Our assessment shows potential for implementing circular economy practices in your operations.",
            "I can help develop a sustainability scorecard for your suppliers.",
            "Let's explore renewable energy options for your warehousing operations."
        ]
    },
    risk_management: {
        keywords: ['risk', 'disruption', 'contingency', 'backup', 'emergency', 'resilience'],
        responses: [
            "I can help develop comprehensive risk mitigation strategies for your supply chain.",
            "Let's create contingency plans for potential supply chain disruptions.",
            "Based on market analysis, I recommend diversifying your supplier base to reduce risks.",
            "Our system can simulate various risk scenarios to test supply chain resilience.",
            "I can help implement real-time risk monitoring and alert systems."
        ]
    },
    cost_optimization: {
        keywords: ['cost', 'expense', 'savings', 'efficiency', 'budget', 'optimization'],
        responses: [
            "Our analysis shows potential cost savings through improved inventory management.",
            "I can help identify and eliminate non-value-adding activities in your supply chain.",
            "Let's analyze transportation costs and suggest optimization strategies.",
            "Our system can help optimize warehouse layout for improved operational efficiency.",
            "I can help implement activity-based costing for better cost control."
        ]
    },
    technology_integration: {
        keywords: ['technology', 'automation', 'digital', 'software', 'system', 'integration'],
        responses: [
            "I can help evaluate and implement suitable supply chain management software solutions.",
            "Let's explore automation opportunities in your warehouse operations.",
            "Our analysis suggests implementing IoT sensors for better inventory tracking.",
            "I can help develop a roadmap for digital transformation of your supply chain.",
            "Let's integrate blockchain technology for better supply chain transparency."
        ]
    }
};

// DOM Elements
const authContainer = document.getElementById('auth-container');
const chatInterface = document.getElementById('chat-interface');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-btn');

// State
let isAuthenticated = false;

// Auth Functions
function toggleAuthForm() {
    loginForm.classList.toggle('hidden');
    registerForm.classList.toggle('hidden');
}

async function handleRegister() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            alert('Registration successful! Please login.');
            toggleAuthForm();
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

async function handleLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            isAuthenticated = true;
            localStorage.setItem('user', JSON.stringify(data.user));
            showChatInterface();
            loadChatHistory();
        } else {
            const errorMessage = data.error || 'Login failed';
            console.error('Login error:', errorMessage);
            alert(errorMessage);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please check your connection and try again.');
    }
}

async function handleLogout() {
    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: 'POST',
            credentials: 'include',
        });

        if (response.ok) {
            isAuthenticated = false;
            showAuthForm();
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Chat Functions
async function handleUserInput() {
    const message = userInput.value.trim();
    if (message === '') return;

    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';

    try {
        // First try to get response from server
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        if (response.ok) {
            addMessage(data.response, 'bot');
        } else {
            // If server returns error, fallback to local knowledge base
            const localResponse = findLocalResponse(message);
            addMessage(localResponse, 'bot');
        }
    } catch (error) {
        console.error('Chat error:', error);
        // If server is unreachable, fallback to local knowledge base
        const localResponse = findLocalResponse(message);
        addMessage(localResponse, 'bot');
    }
}

// Function to find response from local knowledge base
function findLocalResponse(message) {
    const lowercaseMessage = message.toLowerCase();
    
    // Check each category's keywords
    for (const category in knowledgeBase) {
        const { keywords, responses } = knowledgeBase[category];
        
        // If any keyword matches the message
        if (keywords.some(keyword => lowercaseMessage.includes(keyword))) {
            // Return a random response from that category
            const randomIndex = Math.floor(Math.random() * responses.length);
            return responses[randomIndex];
        }
    }
    
    // If no keyword matches, return a default response
    return "I understand you're asking about supply chain management. Could you please be more specific about what aspect you'd like to know about? I can help with inventory, logistics, procurement, forecasting, quality control, sustainability, risk management, cost optimization, or technology integration.";
}

async function loadChatHistory() {
    try {
        const response = await fetch(`${API_URL}/chat-history`);
        const data = await response.json();

        if (response.ok) {
            chatMessages.innerHTML = '';
            data.forEach(chat => {
                addMessage(chat.user_message, 'user');
                addMessage(chat.bot_response, 'bot');
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
        // If can't load chat history, just show welcome message
        chatMessages.innerHTML = '';
        const initialMessage = "Hello! I'm your Supply Chain Assistant. I can help you with inventory management, logistics, procurement, forecasting, quality control, sustainability, risk management, cost optimization, and technology integration. What would you like to know?";
        addMessage(initialMessage, 'bot');
    }
}

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    
    const content = document.createElement('div');
    content.classList.add('message-content');
    content.textContent = message;
    
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// UI Functions
function showChatInterface() {
    authContainer.classList.add('hidden');
    chatInterface.classList.remove('hidden');
}

function showAuthForm() {
    authContainer.classList.remove('hidden');
    chatInterface.classList.add('hidden');
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
}

// Event Listeners
sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

// Add initial bot message and load chat history
window.addEventListener('load', () => {
    const initialMessage = "Hello! I'm your Supply Chain Assistant. I can help you with inventory management, logistics, procurement, and demand forecasting. What would you like to know?";
    addMessage(initialMessage, 'bot');
    loadChatHistory();
}); 