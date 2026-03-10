// import React, { useState } from "react";
// import { Button } from "react-bootstrap";
// import { useNavigate, useSearchParams } from "react-router-dom";
// import "./ChatPage.scss";
// import ApiService, {
//   startConversation,
// } from "../../../../services/Api.service";
// import { PulseLoader } from "react-spinners";

// const ChatPage = () => {
//   let [searchParams] = useSearchParams();

//   const [messages, setMessages] = useState([
//     {
//       question: "",
//       Ai_response: "Hello, How can I help you today?",
//     },
//   ]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   const navigate = useNavigate();

//   const handleSend = async (e) => {
//     e.preventDefault();
//     if (!input.trim()) return;
//     setLoading(true);
 
//     setMessages((prev) => [...prev, { question: input, Ai_response: "" }]);

//     try {
//       let payload = {
//         question: input,
//         namespace_id: searchParams.get("namespace_id"),
//         chatHistory: messages,
//       };
//       setInput("");

//       await startConversation(payload, (chunk) => {
//         const chunkText =
//           typeof chunk === "string"
//             ? chunk
//             : chunk?.text ??
//               chunk?.Ai_response ??
//               chunk?.data ??
//               JSON.stringify(chunk);

//         setMessages((prev) => {
//           const lastIdx = prev.length - 1;

//           if (lastIdx < 0) return prev;

//           const updated = [...prev];
//           const last = { ...updated[lastIdx] };

//           if (last.question === "") {
//             last.Ai_response = (last.Ai_response || "") + chunkText;
//             updated[lastIdx] = last;

//             return updated;
//           }

//           return [...prev, { question: "", Ai_response: chunkText }];
//         });
//       });
//     } catch (err) {
//       console.error("Streaming error:", err);
//       setMessages((prev) => [
//         ...prev,
//         { question: "", Ai_response: "⚠️ Error receiving response." },
//       ]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const formatResponse = (text) => {
//     return text
//       .replace(/For More Reference:/g, "\n\nFor More Reference:\n")
//       .replace(/•/g, "\n•")
//       .replace(/\. /g, ".\n")
//       .replace(/- /g, "\n -")
//       .trim();
//   };

//   return (
//     <div className="chat-page container-fluid py-3">
//       <div className="row justify-content-center">
//         <div className="col-lg-9 col-md-10">
//           <div className="card chat-card shadow-sm rounded-4">
//             <div className="chat-header border-bottom px-4 py-3 d-flex justify-content-between align-items-center">
//               <h5 className="fw-bold text-primary mb-0">🤖</h5>
//               <Button
//                 variant="outline-secondary"
//                 className="rounded-pill px-4"
//                 onClick={() => navigate(-1)}
//               >
//                 ← Back
//               </Button>
//             </div>

//             <div className="chat-body px-3 py-4">
//               {messages.map((msg, index) => (
//                 <div
//                   key={index}
//                   className={`message-row ${
//                     msg.question ? "text-end" : "text-start"
//                   }`}
//                 >
//                   <div
//                     className={`message-bubble ${
//                       msg.question ? "user-msg" : "bot-msg"
//                     }`}
//                   >
//                     {msg.question && (
//                       <div className="font-semibold">{msg.question}</div>
//                     )}

//                     {msg.Ai_response && (
//                       <div
//                         className="whitespace-pre-line text-left"
//                         style={{
//                           whiteSpace: "pre-wrap",
//                           lineHeight: "1.6",
//                         }}
//                       >
//                         {formatResponse(msg.Ai_response)}
//                       </div>
//                     )}
//                   </div>
//                 </div>
//               ))}
//               {loading && (
//                 <div className="text-start mt-2">
//                   <div className="bot-msg d-inline-block px-3 py-1 rounded-4 bg-light">
//                     <PulseLoader
//                       color="#409fffff"
//                       size={8}
//                       margin={3}
//                       speedMultiplier={0.7}
//                     />
//                   </div>
//                 </div>
//               )}
//             </div>

//             <div className="chat-input border-top px-3 py-3">
//               <form className="d-flex gap-2">
//                 <input
//                   type="text"
//                   placeholder="Type your message..."
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   className="form-control rounded-pill px-3"
//                 />
//                 <button
//                   className="btn btn-primary rounded-pill px-4"
//                   onClick={handleSend}
//                   disabled={loading}
//                 >
//                   Send
//                 </button>
//               </form>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ChatPage;

//SAME OUPUT WALA CODE 

import React, { useState, useEffect } from 'react';
import './ChatPage.scss';
import ApiService, { startConversation } from '../../../../services/Api.service';
import { getVariable } from '../../../../utils/localStorage';
import { useSearchParams, useNavigate } from 'react-router-dom';
import ResumeAnalysis from './ResumeAnalysis.jsx';

const ChatPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  // Fresh start - empty messages
  const [messages, setMessages] = useState([
    { id: 1, sender: 'bot', text: 'Hello! I am ResumeXpert Assistant. Upload your resume to get started.' }
  ]);
  
  // Initially empty
  const [skills, setSkills] = useState([]);
  const [score, setScore] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentBot, setCurrentBot] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [backendStatus, setBackendStatus] = useState('checking'); // 'checking', 'online', 'offline'

  // Check backend status on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch('http://localhost:8000/health', { 
          method: 'GET',
          timeout: 3000 
        });
        if (response.ok) {
          setBackendStatus('online');
        } else {
          setBackendStatus('offline');
        }
      } catch (error) {
        setBackendStatus('offline');
      }
    };

    checkBackend();
    // Check every 10 seconds
    const interval = setInterval(checkBackend, 10000);
    return () => clearInterval(interval);
  }, []);

  // Load or create bot on component mount
  useEffect(() => {
    const initializeBot = async () => {
      const namespace_id = searchParams.get('namespace_id');
      if (namespace_id) {
        // Use existing bot
        const bots = await ApiService.getAllChatBots();
        if (bots.data?.result) {
          const bot = bots.data.result.find(b => b.namespace_id === namespace_id);
          if (bot) {
            setCurrentBot(bot);
            return;
          }
        }
      }
      
      // Create new bot
      const botData = {
        name: 'Resume Analyzer',
        description: 'AI-powered resume analysis assistant'
      };
      const result = await ApiService.createChatBot(botData);
      if (result.data?.result) {
        setCurrentBot(result.data.result);
        // Update URL with new namespace_id
        navigate(`/chat?namespace_id=${result.data.result.namespace_id}`, { replace: true });
      }
    };
    
    initializeBot();
  }, [searchParams, navigate]);

  // Handle real file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file || !currentBot) return;
    
    setUploadedFile(file.name);
    
    // Add upload message
    const uploadMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: `Uploading: ${file.name}...` 
    };
    setMessages(prev => [...prev, uploadMsg]);
    
    try {
      setIsAnalyzing(true);
      
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('files', file);
      
      // Upload and analyze with simple API (no external dependencies)
      const response = await fetch('http://localhost:8000/simple-analyzer/upload-and-analyze', {
        method: 'POST',
        body: formData
      });
      
      const result = await response.json();
      
      if (result.success) {
        const successMsg = { 
          id: messages.length + 2, 
          sender: 'bot', 
          text: `✅ ${file.name} analyzed successfully! Score: ${result.score}%` 
        };
        setMessages(prev => [...prev, successMsg]);
        
        // Update analysis data with structured results
        setScore(result.score || 0);
        setSkills(result.skills || []);
        setSuggestions(result.suggestions || {});
        
        const analyzeMsg = { 
          id: messages.length + 3, 
          sender: 'bot', 
          text: '📊 Resume analysis complete! Check the right panel for detailed recommendations.' 
        };
        setMessages(prev => [...prev, analyzeMsg]);
        setIsAnalyzing(false);
      } else {
        throw new Error(result.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      const errorMsg = { 
        id: messages.length + 2, 
        sender: 'bot', 
        text: `❌ Error analyzing file: ${error.message}` 
      };
      setMessages(prev => [...prev, errorMsg]);
      setIsAnalyzing(false);
    }
  };

  const handleGetTips = () => {
    if (!uploadedFile) {
      const noFileMsg = { 
        id: messages.length + 1, 
        sender: 'bot', 
        text: 'Please upload your resume first to get personalized tips.' 
      };
      setMessages([...messages, noFileMsg]);
      return;
    }
    
    const tipsMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: 'Here are personalized resume tips: 1. Use action verbs. 2. Quantify achievements. 3. Tailor for each job. 4. Keep it concise.' 
    };
    setMessages([...messages, tipsMsg]);
  };

  const handleSkillsAdvice = () => {
    if (!uploadedFile) {
      const noFileMsg = { 
        id: messages.length + 1, 
        sender: 'bot', 
        text: 'Please upload your resume first to get skills advice.' 
      };
      setMessages([...messages, noFileMsg]);
      return;
    }
    
    const skillsMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: 'Based on your resume, consider adding these in-demand skills: React, Node.js, AWS, Docker, MongoDB.' 
    };
    setMessages([...messages, skillsMsg]);
  };

  const handleUserMessage = async () => {
    const input = document.querySelector('.chat-input input');
    const text = input.value.trim();
    
    if (!text || !currentBot) return;
    
    // Add user message
    const userMsg = { id: messages.length + 1, sender: 'user', text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    input.value = '';
    
    // Add loading message
    const loadingMsg = { 
      id: messages.length + 2, 
      sender: 'bot', 
      text: '🤔 Thinking...' 
    };
    setMessages(prev => [...prev, loadingMsg]);
    
    try {
      // Call real chat API
      const payload = {
        question: text,
        namespace_id: currentBot.namespace_id,
        chatHistory: chatHistory
      };
      
      let fullResponse = '';
      
      await startConversation(payload, (chunk) => {
        const chunkText = typeof chunk === 'string' ? chunk : chunk?.text || chunk?.Ai_response || JSON.stringify(chunk);
        fullResponse += chunkText;
        
        // Update the loading message with the response
        setMessages(prev => {
          const updated = [...prev];
          const lastIdx = updated.length - 1;
          if (updated[lastIdx]?.sender === 'bot' && updated[lastIdx]?.text === '🤔 Thinking...') {
            updated[lastIdx] = { 
              id: updated[lastIdx].id, 
              sender: 'bot', 
              text: fullResponse || '🤔 Thinking...' 
            };
          } else {
            updated.push({ id: Date.now(), sender: 'bot', text: chunkText });
          }
          return updated;
        });
      });
      
      // Update chat history
      setChatHistory(prev => [...prev, { question: text, Ai_response: fullResponse }]);
      
      // Extract skills and suggestions from response if it's an analysis
      if (text.toLowerCase().includes('analyze') || text.toLowerCase().includes('skill')) {
        extractAnalysisData(fullResponse);
      }
      
    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg = { 
        id: messages.length + 3, 
        sender: 'bot', 
        text: '❌ Sorry, I encountered an error. Please try again.' 
      };
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = errorMsg; // Replace loading message
        return updated;
      });
    }
  };
  
  // Extract analysis data from AI response
  const extractAnalysisData = (response) => {
    try {
      // Simple extraction - in real implementation, you might want more sophisticated parsing
      const lines = response.split('\n');
      const skillsFound = [];
      const suggestionsFound = [];
      
      lines.forEach(line => {
        // Look for skills
        if (line.toLowerCase().includes('skill') && line.includes(':')) {
          const skillsText = line.split(':')[1];
          if (skillsText) {
            const skills = skillsText.split(',').map(s => s.trim().replace(/[-•*]/g, '')).filter(s => s);
            skillsFound.push(...skills);
          }
        }
        
        // Look for suggestions
        if (line.toLowerCase().includes('suggest') || line.toLowerCase().includes('improve')) {
          suggestionsFound.push(line.trim());
        }
        
        // Look for score
        const scoreMatch = line.match(/(\d+)%/);
        if (scoreMatch) {
          setScore(parseInt(scoreMatch[1]));
        }
      });
      
      if (skillsFound.length > 0) {
        setSkills(skillsFound.slice(0, 10)); // Limit to 10 skills
      }
      
      if (suggestionsFound.length > 0) {
        setSuggestions(suggestionsFound.slice(0, 5)); // Limit to 5 suggestions
      }
    } catch (error) {
      console.error('Error extracting analysis data:', error);
    }
  };

  // Hidden file input
  const triggerFileInput = () => {
    document.getElementById('resumeUpload').click();
  };

  return (
    <div className="chat-page">
      <div className="container-fluid">
        <h1 className="main-title">
          <i className="fas fa-binoculars"></i> ResumeXpert – AI Driven Resume Analyzer
        </h1>
        
        <div className="row">
          {/* LEFT PANEL - CHAT ASSISTANT */}
          <div className="col-lg-6">
            <div className="card shadow-lg">
              <div className="card-header assistant-header">
                <h3><i className="fas fa-robot"></i> ResumeXpert Assistant</h3>
                <div className="online-dot"></div>
              </div>
              <div className="card-body">
                {/* Action Buttons */}
                <div className="action-buttons">
                  <button className="action-btn upload-btn" onClick={triggerFileInput}>
                    <i className="fas fa-upload"></i> Upload Resume
                  </button>
                  <input 
                    type="file" 
                    id="resumeUpload" 
                    style={{ display: 'none' }}
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileUpload}
                  />
                  
                  <button className="action-btn tips-btn" onClick={handleGetTips}>
                    <i className="fas fa-lightbulb"></i> Get Tips
                  </button>
                  
                  <button className="action-btn skills-btn" onClick={handleSkillsAdvice}>
                    <i className="fas fa-tools"></i> Skills Advice
                  </button>
                </div>

                {/* Backend Status Indicator */}
                <div className="backend-status" style={{
                  padding: '8px 12px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  marginBottom: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  {backendStatus === 'checking' && (
                    <>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: '#fbbf24',
                        animation: 'pulse 1.5s infinite'
                      }}></div>
                      <span style={{ color: '#92400e' }}>Checking backend status...</span>
                    </>
                  )}
                  {backendStatus === 'online' && (
                    <>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: '#10b981'
                      }}></div>
                      <span style={{ color: '#065f46' }}>✅ Backend online - Ready to analyze resumes</span>
                    </>
                  )}
                  {backendStatus === 'offline' && (
                    <>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: '#ef4444'
                      }}></div>
                      <span style={{ color: '#991b1b' }}>
                        ❌ Backend offline - 
                        <button 
                          onClick={() => window.open('d:\\Windsurf\\Hire lens FYP\\hire_lens-dev\\start_backend.bat')}
                          style={{
                            background: 'none',
                            border: 'none',
                            color: '#3b82f6',
                            textDecoration: 'underline',
                            cursor: 'pointer',
                            marginLeft: '4px'
                          }}
                        >
                          Click here to start backend
                        </button>
                      </span>
                    </>
                  )}
                </div>

                {/* Upload Status */}
                {uploadedFile && (
                  <div className="upload-status">
                    <i className="fas fa-file-pdf"></i>
                    <span>Current file: {uploadedFile}</span>
                  </div>
                )}

                {/* Chat Messages */}
                <div className="chat-messages">
                  {messages.map(msg => (
                    <div 
                      key={msg.id} 
                      className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
                    >
                      <div className="message-content">
                        <strong>{msg.sender === 'user' ? 'You' : 'ResumeXpert'}:</strong> {msg.text}
                      </div>
                    </div>
                  ))}
                  {isAnalyzing && (
                    <div className="message bot-message">
                      <div className="message-content">
                        <strong>ResumeXpert:</strong> 
                        <i className="fas fa-spinner fa-spin" style={{marginLeft: '10px'}}></i> Analyzing resume content...
                      </div>
                    </div>
                  )}
                </div>

                {/* Chat Input */}
                <div className="chat-input">
                  <input 
                    type="text" 
                    placeholder="Type your message here..." 
                    onKeyPress={(e) => e.key === 'Enter' && handleUserMessage()}
                  />
                  <button className="send-btn" onClick={handleUserMessage}>
                    <i className="fas fa-paper-plane"></i> Send
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* RIGHT PANEL - DYNAMIC ANALYSIS */}
          <div className="col-lg-6">
            <ResumeAnalysis 
              score={score}
              skills={skills}
              suggestions={suggestions}
              fileName={uploadedFile}
              experience="Entry-level / Fresher"
              education="Not specified"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;