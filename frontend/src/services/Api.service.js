import AxiosClient from "./Axios.service.js";
import qs from "qs";
import { setVariable } from "../utils/localStorage.js";
import { apiBaseUrl } from '../constants/constant.js';  
import { getVariable } from '../utils/localStorage.js';

const ApiService = {
  login: async (payload) => {
    const { data, loading, error } = await AxiosClient({
      method: "POST",
      url: `user/login`,
      data: payload,
    });
    if (data ) {
      setVariable("km_user_token", data.result.token);
    }
    return { data, error, loading };
  },

   register: async (payload) => {
    const { data, loading, error } = await AxiosClient({
      method: "POST",
      url: `user/register`,
      data: payload,
    });
    
    return { data, error, loading };
  },

   getAllChatBots: async () => {
    const { data, loading, error } = await AxiosClient({
      method: "GET",
      url: `chat-bot/all`,
    });
    
    return { data, error, loading };
  },

   createChatBot: async (payload) => {
    const { data, loading, error } = await AxiosClient({
      method: "POST",
      url: `chat-bot/`,
      data:payload
    });
    
    return { data, error, loading };
  },

  //  startConversation: async (payload) => {
  //   const { data, loading, error } = await AxiosClient({
  //     method: "POST",
  //     url: `chat-bot/chat`,
  //     data:payload
  //   });
    
  //   return { data, error, loading };
  // },

   getAllFiles: async (chatBotId) => {
    const { data, loading, error } = await AxiosClient({
      method: "GET",
      url: `files?chatBotId=${chatBotId}`
    });
    
    return { data, error, loading };
  },

  uploadFile: async (payload) => {
    const { data, loading, error } = await AxiosClient({
      method: "POST",
      url: `files/fileUpload`,
      data:payload,
      contentType:'multipart/form-data'
    });
    
    return { data, error, loading };
  },
  deleteFile: async (payload) => {
    const { data, loading, error } = await AxiosClient({
      method: "DELETE",
      url: `files/file`,
      data:payload
    });
    
    return { data, error, loading };
  },

  
};

/**
 * Streams conversation response and calls onChunk for each parsed chunk.
 * onChunk receives either a string or parsed object depending on server.
 */
export const startConversation = async (payload, onChunk) => {
  const token = getVariable('km_user_token');

  const response = await fetch(`${apiBaseUrl}chat-bot/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Network error: ${response.status} ${response.statusText}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunkStr = decoder.decode(value, { stream: true });
      buffer += chunkStr;
 
      const parts = buffer.split('\n');
      buffer = parts.pop();

      for (const part of parts) {
        const line = part.trim();
        if (!line) continue;

 
        const jsonString = line.startsWith('data:') ? line.replace(/^data:\s*/, '') : line;

     
        try {
          const parsed = JSON.parse(jsonString);
          onChunk(parsed);
        } catch (err) {
          
          onChunk(jsonString);
        }
      }
    }

 
    if (buffer && buffer.trim()) {
      const remaining = buffer.trim();
      try {
        onChunk(JSON.parse(remaining));
      } catch {
        onChunk(remaining);
      }
    }
  } finally {
    try { reader.releaseLock(); } catch (e) {}
  }
};

export default ApiService;

// // 📄 src/services/Api.service.js
// import AxiosClient from "./Axios.service.js";
// import { setVariable } from "../utils/localStorage.js";
// import { apiBaseUrl } from '../constants/constant.js';  
// import { getVariable } from '../utils/localStorage.js';

// const ApiService = {
//   login: async (payload) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `user/login`,
//       data: payload,
//     });
//     if (data) {
//       setVariable("km_user_token", data.result.token);
//     }
//     return { data, error, loading };
//   },

//   register: async (payload) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `user/register`,
//       data: payload,
//     });
    
//     return { data, error, loading };
//   },

//   getAllChatBots: async () => {
//     const { data, loading, error } = await AxiosClient({
//       method: "GET",
//       url: `chat-bot/all`,
//     });
    
//     return { data, error, loading };
//   },

//   createChatBot: async (payload) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `chat-bot/`,
//       data: payload
//     });
    
//     return { data, error, loading };
//   },

//   getAllFiles: async (chatBotId) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "GET",
//       url: `files?chatBotId=${chatBotId}`
//     });
    
//     return { data, error, loading };
//   },

//   uploadFile: async (payload) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `files/fileUpload`,
//       data: payload,
//       contentType: 'multipart/form-data'
//     });
    
//     return { data, error, loading };
//   },

//   deleteFile: async (payload) => {
//     const { data, loading, error } = await AxiosClient({
//       method: "DELETE",
//       url: `files/file`,
//       data: payload
//     });
    
//     return { data, error, loading };
//   },

//   // ✅ NEW: Resume Analysis Function
//   analyzeResume: async (formData) => {
//     try {
//       const token = getVariable('km_user_token');
      
//       const response = await fetch(`${apiBaseUrl}resume/analyze`, {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`,
//         },
//         body: formData,
//       });

//       if (!response.ok) {
//         throw new Error(`Analysis failed: ${response.status}`);
//       }

//       const data = await response.json();
//       return data;
      
//     } catch (error) {
//       console.log('Using mock resume data for demo...');
      
//       // ✅ MOCK DATA for demo
//       return {
//         success: true,
//         score: Math.floor(Math.random() * 20) + 75, // 75-95 random
//         skills: [
//           { name: "HTML", level: "Advanced", category: "Frontend" },
//           { name: "CSS", level: "Advanced", category: "Frontend" },
//           { name: "JavaScript", level: "Intermediate", category: "Frontend" },
//           { name: "SQL", level: "Intermediate", category: "Database" },
//           { name: "Salesforce", level: "Beginner", category: "CRM" },
//           { name: "Python", level: "Learning", category: "Backend" }
//         ],
//         projects: [
//           {
//             name: "Student Management System",
//             description: "Centralized system for managing student data using web technologies",
//             technologies: ["HTML", "CSS", "JavaScript", "SQL", "Salesforce"],
//             impact: "Streamlined student data management process"
//           }
//         ],
//         suggestions: [
//           "Add details about Python training (duration, projects, certification)",
//           "Include quantifiable achievements in projects",
//           "Add GitHub profile link with code samples",
//           "Mention soft skills like communication and teamwork",
//           "Add relevant certifications if available"
//         ],
//         missingKeywords: ["React", "Node.js", "Git", "REST API", "Agile"],
//         education: "Currently pursuing Python Programming training",
//         experience: "Fresher / Entry Level",
//         overallFeedback: "Good foundation in web development. Focus on adding more technical depth and project details.",
//         improvementAreas: [
//           "Technical Skills Depth",
//           "Project Documentation",
//           "Quantifiable Achievements",
//           "Professional Certifications"
//         ]
//       };
//     }
//   },

//   // ✅ NEW: Get Job Recommendations
//   getJobRecommendations: async (resumeData) => {
//     const token = getVariable('km_user_token');
    
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `jobs/recommend`,
//       data: resumeData,
//       headers: {
//         'Authorization': `Bearer ${token}`
//       }
//     });
    
//     return { data, error, loading };
//   },

//   // ✅ NEW: Generate Improved Resume
//   generateImprovedResume: async (resumeText) => {
//     const token = getVariable('km_user_token');
    
//     const { data, loading, error } = await AxiosClient({
//       method: "POST",
//       url: `resume/enhance`,
//       data: { resume: resumeText },
//       headers: {
//         'Authorization': `Bearer ${token}`
//       }
//     });
    
//     return { data, error, loading };
//   }
// };

// /**
//  * Streams conversation response
//  */
// export const startConversation = async (payload, onChunk) => {
//   const token = getVariable('km_user_token');

//   const response = await fetch(`${apiBaseUrl}chat-bot/chat`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       Authorization: `Bearer ${token}`,
//     },
//     body: JSON.stringify(payload),
//   });

//   if (!response.ok) {
//     throw new Error(`Network error: ${response.status} ${response.statusText}`);
//   }

//   const reader = response.body.getReader();
//   const decoder = new TextDecoder('utf-8');
//   let buffer = '';

//   try {
//     while (true) {
//       const { done, value } = await reader.read();
//       if (done) break;

//       const chunkStr = decoder.decode(value, { stream: true });
//       buffer += chunkStr;
 
//       const parts = buffer.split('\n');
//       buffer = parts.pop();

//       for (const part of parts) {
//         const line = part.trim();
//         if (!line) continue;

//         const jsonString = line.startsWith('data:') ? line.replace(/^data:\s*/, '') : line;

//         try {
//           const parsed = JSON.parse(jsonString);
//           onChunk(parsed);
//         } catch (err) {
//           onChunk(jsonString);
//         }
//       }
//     }

//     if (buffer && buffer.trim()) {
//       const remaining = buffer.trim();
//       try {
//         onChunk(JSON.parse(remaining));
//       } catch {
//         onChunk(remaining);
//       }
//     }
//   } finally {
//     try { reader.releaseLock(); } catch (e) {}
//   }
// };


