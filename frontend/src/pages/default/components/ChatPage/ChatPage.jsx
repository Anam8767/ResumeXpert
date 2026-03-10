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

import React, { useState } from 'react';
import './ChatPage.scss';
import axios from 'axios';

const ChatPage = () => {
  // Fresh start - empty messages
  const [messages, setMessages] = useState([
    { id: 1, sender: 'bot', text: 'Hello! I am ResumeXpert Assistant. Upload your resume to get started.' }
  ]);
  
  // Initially empty
  const [skills, setSkills] = useState([]);
  const [score, setScore] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const [jobRoles, setJobRoles] = useState([]);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileUrl, setFileUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Handle file upload with SIMPLE API integration (no external APIs needed)
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      // Clear all previous data immediately
      setUploadedFile(null);
      setFileUrl(null);
      setScore(0);
      setSkills([]);
      setSuggestions([]);
      setJobRoles([]);
      setIsAnalyzing(true);
      
      // Clear chat history except welcome message
      setMessages([
        { id: 1, sender: 'bot', text: '📄 New resume uploaded! Analyzing your document...' }
      ]);
      
      // Set new file name
      setUploadedFile(file.name);
      
      // Create file URL for viewing
      const url = URL.createObjectURL(file);
      setFileUrl(url);
      
      // Add message
      const uploadMsg = { 
        id: 2, 
        sender: 'bot', 
        text: `📄 Resume "${file.name}" uploaded successfully! Starting analysis...` 
      };
      setMessages(prev => [...prev, uploadMsg]);
      
      // Start REAL analysis
      const analyzingMsg = { 
        id: 3, 
        sender: 'bot', 
        text: '🔍 Analyzing your resume with AI...' 
      };
      setMessages(prev => [...prev, analyzingMsg]);
      
      try {
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
          // Update dashboard with real results
          setScore(result.score);
          setSkills(result.skills);
          setSuggestions(result.suggestions);
          setJobRoles(result.job_roles || []);
          
          // Success message
          const successMsg = { 
            id: 4, 
            sender: 'bot', 
            text: `✅ Analysis Complete! Score: ${result.score}%. Found ${result.skills.length} skills. Check dashboard for details!` 
          };
          setMessages(prev => [...prev.slice(0, -1), successMsg]);
          
        } else {
          throw new Error(result.error || 'Analysis failed');
        }
        
      } catch (error) {
        console.error('Upload/Analysis error:', error.message)
        const errorMsg = { 
          id: 4, 
          sender: 'bot', 
          text: `❌ Error analyzing resume: ${error.message}. Please try again.` 
        };
        setMessages(prev => [...prev.slice(0, -1), errorMsg]);
      } finally {
        setIsAnalyzing(false);
      }
    }
  };

  const handleGetTips = () => {
    if (!uploadedFile) {
      const noFileMsg = { 
        id: messages.length + 1, 
        sender: 'bot', 
        text: 'Please upload your resume first to get personalized tips.' 
      };
      setMessages(prev => [...prev, noFileMsg]);
      return;
    }
    
    // Generate personalized tips based on actual resume analysis
    const personalizedTips = [];
    const tipPriority = [];
    const tipImpact = [];
    const tipTimeframe = [];
    
    // Check score and give specific tips
    if (score < 50) {
      personalizedTips.push("🔴 Your resume needs major improvements. Add more skills, experience details, and projects.");
      tipPriority.push("CRITICAL");
      tipImpact.push("Could improve score by 20-30 points");
      tipTimeframe.push("Immediate action required");
    } else if (score < 70) {
      personalizedTips.push("🟡 Good foundation! Add specific achievements and quantify your results.");
      tipPriority.push("HIGH");
      tipImpact.push("Could improve score by 10-15 points");
      tipTimeframe.push("1-2 weeks");
    } else {
      personalizedTips.push("🟢 Strong resume! Highlight leadership experience and advanced skills.");
      tipPriority.push("MEDIUM");
      tipImpact.push("Could improve score by 5-10 points");
      tipTimeframe.push("2-3 weeks");
    }
    
    // Skills-based tips
    if (skills.length < 5) {
      personalizedTips.push("📚 Add more technical skills. List specific technologies you've worked with.");
      tipPriority.push("HIGH");
      tipImpact.push("Adds 10-15 points to score");
      tipTimeframe.push("1 week");
    } else if (skills.length < 10) {
      personalizedTips.push("💪 Good skills! Add 2-3 more advanced or specialized technologies.");
      tipPriority.push("MEDIUM");
      tipImpact.push("Adds 5-10 points to score");
      tipTimeframe.push("2 weeks");
    }
    
    // Check for missing sections
    if (!suggestions.some(s => s.includes('experience'))) {
      personalizedTips.push("💼 Add detailed work experience with specific achievements and metrics.");
      tipPriority.push("HIGH");
      tipImpact.push("Adds 10-20 points to score");
      tipTimeframe.push("1-2 weeks");
    }
    
    if (!suggestions.some(s => s.includes('project'))) {
      personalizedTips.push("🚀 Include 2-3 specific projects with technologies used and outcomes.");
      tipPriority.push("HIGH");
      tipImpact.push("Adds 8-15 points to score");
      tipTimeframe.push("1 week");
    }
    
    // Check for common missing elements
    if (!suggestions.some(s => s.includes('github'))) {
      personalizedTips.push("🔗 Add GitHub profile link to showcase your coding projects.");
      tipPriority.push("MEDIUM");
      tipImpact.push("Adds 3-5 points to score");
      tipTimeframe.push("1 day");
    }
    
    if (!suggestions.some(s => s.includes('linkedin'))) {
      personalizedTips.push("🌐 Include LinkedIn profile for professional networking.");
      tipPriority.push("LOW");
      tipImpact.push("Adds 2-3 points to score");
      tipTimeframe.push("1 day");
    }
    
    // Add formatting tips
    personalizedTips.push("📝 Use action verbs like 'Developed', 'Implemented', 'Led' instead of passive language.");
    tipPriority.push("MEDIUM");
    tipImpact.push("Adds 5-8 points to score");
    tipTimeframe.push("2-3 days");
    
    personalizedTips.push("📊 Quantify achievements with numbers (e.g., 'Improved performance by 30%').");
    tipPriority.push("HIGH");
    tipImpact.push("Adds 8-12 points to score");
    tipTimeframe.push("3-5 days");
    
    // Create systematic tips message
    const tipsMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: `🎯 **Personalized Resume Tips Based on Your Analysis:**

**Current Resume Score:** ${score}/100

**📈 Actionable Improvement Tips:**

${personalizedTips.map((tip, index) => 
  `**${index + 1}. ${tip}**
🎯 Priority: ${tipPriority[index]}
� Impact: ${tipImpact[index]}
⏱️ Timeframe: ${tipTimeframe[index]}
🔧 How to Implement:
${tipPriority[index] === 'CRITICAL' ? '   • Focus on this immediately\n   • This is blocking your resume success\n   • Maximum impact on overall score' : tipPriority[index] === 'HIGH' ? '   • Start working on this this week\n   • Significant impact on resume quality\n   • Quick wins for improvement' : tipPriority[index] === 'MEDIUM' ? '   • Plan for next 2-3 weeks\n   • Good for overall enhancement\n   • Steady improvement strategy' : '   • Nice to have improvements\n   • Minor impact but good to have\n   • Professional polish'}

---`
).join('')}

**🚀 Quick Action Plan:**
• **Week 1**: Focus on ${personalizedTips.filter((_, i) => tipPriority[i] === 'HIGH' || tipPriority[i] === 'CRITICAL').length} HIGH/CRIORITY tips
• **Week 2**: Complete ${personalizedTips.filter((_, i) => tipPriority[i] === 'MEDIUM').length} MEDIUM priority improvements  
• **Week 3**: Add ${personalizedTips.filter((_, i) => tipPriority[i] === 'LOW').length} LOW priority polish

**� Expected Transformation:**
• Resume score: ${score} → ${Math.min(100, score + 25)}+
• Interview calls: 2-3x increase
• Job responses: 50-70% improvement
• Salary negotiations: Better positioning

**💡 Pro Tips:**
• Add ${skills.length + 2}+ technical skills to reach optimal level
• Include 2-3 quantified achievements
• Add GitHub/LinkedIn links if missing
• Use action verbs throughout resume` 
    };
    setMessages(prev => [...prev, tipsMsg]);
  };

  const handleSkillsAdvice = () => {
    if (!uploadedFile) {
      const noFileMsg = { 
        id: messages.length + 1, 
        sender: 'bot', 
        text: 'Please upload your resume first to get skills advice.' 
      };
      setMessages(prev => [...prev, noFileMsg]);
      return;
    }
    
    // Generate personalized skills suggestions based on current skills
    const currentSkills = skills.map(s => s.toLowerCase());
    const skillsToAdd = [];
    const skillsReasons = [];
    const skillsImpact = [];
    const skillsPriority = [];
    
    // Check for missing programming languages
    const programmingLanguages = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust'];
    const missingProgramming = programmingLanguages.filter(lang => !currentSkills.includes(lang));
    if (missingProgramming.length > 0) {
      skillsToAdd.push(missingProgramming.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('High-demand programming languages for better job opportunities');
      skillsImpact.push('Could increase salary by 15-25%');
      skillsPriority.push('HIGH');
    }
    
    // Check for web technologies
    const webTech = ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'];
    const missingWebTech = webTech.filter(tech => !currentSkills.includes(tech));
    if (missingWebTech.length > 0) {
      skillsToAdd.push(missingWebTech.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('Modern web frameworks for full-stack development');
      skillsImpact.push('Opens doors to full-stack positions');
      skillsPriority.push('HIGH');
    }
    
    // Check for cloud technologies
    const cloudTech = ['aws', 'azure', 'gcp', 'docker', 'kubernetes'];
    const missingCloudTech = cloudTech.filter(tech => !currentSkills.includes(tech));
    if (missingCloudTech.length > 0) {
      skillsToAdd.push(missingCloudTech.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('Cloud skills are in high demand and offer better salaries');
      skillsImpact.push('Could increase salary by 20-30%');
      skillsPriority.push('MEDIUM');
    }
    
    // Check for databases
    const databases = ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'];
    const missingDatabases = databases.filter(db => !currentSkills.includes(db));
    if (missingDatabases.length > 0) {
      skillsToAdd.push(missingDatabases.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('Database knowledge is essential for most development roles');
      skillsImpact.push('Makes you more versatile as a developer');
      skillsPriority.push('MEDIUM');
    }
    
    // Check for DevOps tools
    const devOpsTools = ['git', 'jenkins', 'terraform', 'ansible', 'ci/cd'];
    const missingDevOps = devOpsTools.filter(tool => !currentSkills.includes(tool));
    if (missingDevOps.length > 0) {
      skillsToAdd.push(missingDevOps.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('DevOps skills make you more valuable to employers');
      skillsImpact.push('Sets you apart from other candidates');
      skillsPriority.push('LOW');
    }
    
    // Check for testing
    const testingTools = ['jest', 'pytest', 'selenium', 'cypress'];
    const missingTesting = testingTools.filter(tool => !currentSkills.includes(tool));
    if (missingTesting.length > 0) {
      skillsToAdd.push(missingTesting.slice(0, 2).join(', ').toUpperCase());
      skillsReasons.push('Testing skills show code quality awareness');
      skillsImpact.push('Demonstrates professional development practices');
      skillsPriority.push('LOW');
    }
    
    // Create systematic skills message
    const skillsMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: `🚀 **Personalized Skills Recommendations Based on Your Resume:**

**Your Current Skills (${skills.length}):** ${skills.join(', ')}

**📈 Skills to Add for Better Opportunities:**

${skillsToAdd.map((skillGroup, index) => 
  `**${index + 1}. ${skillGroup}**
� ${skillsReasons[index]}
� ${skillsImpact[index]}
🎯 Priority: ${skillsPriority[index]}
⏱️ Learning Time: ${skillsPriority[index] === 'HIGH' ? '2-3 months' : skillsPriority[index] === 'MEDIUM' ? '1-2 months' : '2-4 weeks'}
🔧 Key Benefits:
${skillsPriority[index] === 'HIGH' ? '   • Opens doors to more job opportunities\n   • Increases salary potential significantly\n   • Most in-demand skills in market' : skillsPriority[index] === 'MEDIUM' ? '   • Makes you more versatile\n   • Good for career growth\n   • Moderately in-demand' : '   • Sets you apart from competition\n   • Shows professional approach\n   • Nice to have skills'}

---`
).join('')}

**🎯 Learning Strategy:**
• Focus on ${skillsToAdd.slice(0, 2).length} HIGH priority skills first
• Start with skills related to your current expertise
• Add one cloud skill (AWS/Docker) for maximum impact
• Include one testing framework to show quality awareness

**� Expected Results:** 
• Resume score improvement: +${Math.min(25, 100 - score)}%
• Salary increase: 15-30%
• Job opportunities: 2x more interviews
• Career growth: Faster promotion track` 
    };
    setMessages(prev => [...prev, skillsMsg]);
  };

  const handleJobRole = () => {
    if (!uploadedFile) {
      const noFileMsg = { 
        id: messages.length + 1, 
        sender: 'bot', 
        text: 'Please upload your resume first to get job role recommendations.' 
      };
      setMessages(prev => [...prev, noFileMsg]);
      return;
    }
    
    // Create detailed job role message with real data
    const jobRoleMsg = { 
      id: messages.length + 1, 
      sender: 'bot', 
      text: `🎯 **Job Recommendations Based on Your Resume:**

${jobRoles.length > 0 ? jobRoles.map((role, index) => {
      const roleData = typeof role === 'object' ? role : { title: role, description: 'Based on your skills' };
      return `**${index + 1}. ${roleData.title}**
📋 ${roleData.description}
💰 Salary: ${roleData.salary_range || '₹6-12 LPA'}
📈 Level: ${roleData.experience_level || 'Mid Level'}
🔧 Key Responsibilities:
${roleData.responsibilities ? roleData.responsibilities.map(r => `   • ${r}`).join('\n') : '   • Technical development and problem-solving'}

---`;
    }).join('\n') : 'Upload your resume to get personalized job recommendations'}

💡 **Tip**: These roles are specifically matched to your skills and experience. Focus on roles that align with your strongest skills!` 
    };
    setMessages(prev => [...prev, jobRoleMsg]);
  };

  const handleUserMessage = () => {
    const input = document.querySelector('.chat-input input');
    const text = input.value.trim();
    
    if (text) {
      // Add user message
      const userMsg = { id: messages.length + 1, sender: 'user', text };
      setMessages(prev => [...prev, userMsg]);
      input.value = '';
      
      // Bot response
      setTimeout(() => {
        let botResponse = '';
        
        if (text.toLowerCase().includes('upload') || text.toLowerCase().includes('resume')) {
          botResponse = 'Please use the "Upload Resume" button above to upload your file.';
        } else if (text.toLowerCase().includes('tip')) {
          botResponse = 'I can provide resume tips after you upload your resume.';
        } else if (text.toLowerCase().includes('skill')) {
          botResponse = 'I can analyze skills from your uploaded resume.';
        } else if (text.toLowerCase().includes('analyze') || text.toLowerCase().includes('scan')) {
          if (uploadedFile) {
            botResponse = 'Your resume has been analyzed. Check the dashboard for results.';
          } else {
            botResponse = 'Please upload your resume first to analyze it.';
          }
        } else {
          botResponse = 'I can help you with resume analysis, tips, and skills advice. Please upload your resume to get started.';
        }
        
        const botMsg = { id: messages.length + 2, sender: 'bot', text: botResponse };
        setMessages(prev => [...prev, botMsg]);
      }, 500);
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

                {/* Upload Status */}
                {uploadedFile && (
                  <div className="upload-status">
                    <i className="fas fa-file-pdf"></i>
                    <span>Current file: {uploadedFile}</span>
                    <button className="view-resume-btn" onClick={() => window.open(fileUrl, '_blank')}>
                      <i className="fas fa-eye"></i> View
                    </button>
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

                              </div>
            </div>
          </div>

          {/* RIGHT PANEL - DASHBOARD */}
          <div className="col-lg-6">
            <div className="card shadow-lg">
              <div className="card-header dashboard-header">
                <h3><i className="fas fa-tachometer-alt"></i> Dashboard</h3>
                <button className="refresh-btn" onClick={() => window.location.reload()}>
                  <i className="fas fa-redo"></i> Reset
                </button>
              </div>
              <div className="card-body">
                <h4 className="dashboard-title">Resume Dashboard</h4>

                {/* Upload Prompt if no file */}
                {!uploadedFile ? (
                  <div className="empty-dashboard">
                    <i className="fas fa-file-upload" style={{fontSize: '60px', color: '#ccc', marginBottom: '20px'}}></i>
                    <h5>No Resume Uploaded</h5>
                    <p>Upload your resume to see analysis results</p>
                    <button className="action-btn upload-btn" onClick={triggerFileInput} style={{width: 'auto'}}>
                      <i className="fas fa-upload"></i> Upload Resume
                    </button>
                  </div>
                ) : (
                  <>
                    {/* OVERALL SCORE */}
                    <div className="score-section">
                      <h5>Overall Score</h5>
                      <div className="score-circle">
                        <div className="score-text">{score}%</div>
                      </div>
                      <div className="score-label">
                        {score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : 'Needs Improvement'}
                      </div>
                    </div>

                    {/* SKILLS IDENTIFIED */}
                    <div className="skills-section">
                      <h5>Technical Skills Analysis</h5>
                      {skills.length > 0 ? (
                        <div className="skills-cards-list">
                          {skills.map((skill, index) => {
                            // Categorize skills
                            const category = ['Python', 'Java', 'Javascript', 'Typescript', 'C++', 'C#', 'Go', 'Rust'].includes(skill) ? 'Programming' :
                                           ['React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask'].includes(skill) ? 'Web Framework' :
                                           ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform'].includes(skill) ? 'Cloud/DevOps' :
                                           ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch'].includes(skill) ? 'Database' :
                                           ['Tensorflow', 'Pytorch', 'Pandas', 'Numpy', 'Scikit-learn'].includes(skill) ? 'Data Science' :
                                           ['Android', 'iOS', 'Flutter', 'React Native'].includes(skill) ? 'Mobile' : 'Other';
                            
                            const level = ['AWS', 'Docker', 'Kubernetes', 'Tensorflow', 'Pytorch'].includes(skill) ? 'Advanced' :
                                         ['React', 'Node.js', 'Python', 'MongoDB'].includes(skill) ? 'Intermediate' : 'Foundation';
                            
                            const demand = ['AWS', 'React', 'Python', 'Docker', 'Kubernetes', 'Tensorflow'].includes(skill) ? 'High Demand' :
                                         ['JavaScript', 'Java', 'MySQL', 'PostgreSQL'].includes(skill) ? 'Medium Demand' : 'Growing';
                            
                            return (
                              <div key={index} className="skill-card">
                                <div className="skill-header">
                                  <h6>{skill}</h6>
                                  <span className={`level-badge level-${level.toLowerCase().replace(' ', '-')}`}>{level}</span>
                                </div>
                                <div className="skill-category">
                                  <span className="category-tag">{category}</span>
                                  <span className="demand-tag">{demand}</span>
                                </div>
                                <div className="skill-details">
                                  <small className="skill-impact">🎯 {demand}</small>
                                  <small className="skill-level">📊 {level}</small>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        <p className="text-muted">No skills identified yet</p>
                      )}
                    </div>

                    {/* JOB ROLES */}
                    <div className="job-roles-section">
                      <h5>Recommended Job Roles</h5>
                      {jobRoles.length > 0 ? (
                        <div className="job-roles-list">
                          {jobRoles.map((role, index) => {
                            const roleData = typeof role === 'object' ? role : { title: role, description: 'Based on your skills' };
                            return (
                              <div key={index} className="job-role-card">
                                <div className="job-role-header">
                                  <h6>{roleData.title}</h6>
                                  <span className="salary-badge">{roleData.salary_range || '₹6-12 LPA'}</span>
                                </div>
                                <p className="job-description">{roleData.description}</p>
                                <div className="job-details">
                                  <small className="experience-level">📈 {roleData.experience_level || 'Mid Level'}</small>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        <p className="text-muted">Upload resume to get job recommendations</p>
                      )}
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;