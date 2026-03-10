import React from 'react';
import './ResumeAnalysis.css';

const ResumeAnalysis = ({ score = 0, skills = [], suggestions = {}, fileName = '', experience = '', education = '' }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#059669';
    if (score >= 60) return '#d97706';
    return '#dc2626';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    return 'Critical';
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
      padding: '30px',
      margin: '10px 0'
    }}>
      <h1 style={{ 
        color: '#2563eb', 
        textAlign: 'center', 
        fontSize: '28px',
        marginBottom: '10px'
      }}>
        📋 Resume Analysis Report
      </h1>
      
      <div style={{
        textAlign: 'center',
        fontSize: '24px',
        fontWeight: 'bold',
        color: getScoreColor(score),
        background: '#ecfdf5',
        padding: '15px',
        borderRadius: '10px',
        marginBottom: '20px'
      }}>
        {score}% Job Match Score
      </div>
      
      {/* Show skills if available */}
      {skills.length > 0 && (
        <div style={{ marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#1e40af', 
            borderBottom: '3px solid #dbeafe',
            paddingBottom: '10px',
            fontSize: '22px'
          }}>
            🔍 Key Skills Identified
          </h2>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '10px',
            margin: '15px 0'
          }}>
            {skills.slice(0, 8).map((skill, index) => (
              <span key={index} style={{
                background: '#eff6ff',
                color: '#1e40af',
                padding: '8px 16px',
                borderRadius: '25px',
                fontWeight: 'bold',
                fontSize: '14px'
              }}>{skill}</span>
            ))}
            {skills.length > 8 && (
              <span style={{
                background: '#fef3c7',
                color: '#f59e0b',
                padding: '8px 16px',
                borderRadius: '25px',
                fontWeight: 'bold',
                fontSize: '14px'
              }}>+{skills.length - 8} more</span>
            )}
          </div>
        </div>
      )}
      
      {/* Show suggestions if available */}
      {suggestions.length > 0 && (
        <div style={{ marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#1e40af', 
            borderBottom: '3px solid #dbeafe',
            paddingBottom: '10px',
            fontSize: '22px'
          }}>
            💡 Recommendations
          </h2>
          <ul style={{ lineHeight: '1.6', paddingLeft: '20px' }}>
            {suggestions.slice(0, 5).map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Show file name if available */}
      {fileName && (
        <div style={{ marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#1e40af', 
            borderBottom: '3px solid #dbeafe',
            paddingBottom: '10px',
            fontSize: '22px'
          }}>
            📄 Resume Details
          </h2>
          <p style={{ fontSize: '16px', color: '#475569' }}>
            <strong>File:</strong> {fileName}
          </p>
        </div>
      )}
      
      {/* Show experience if available */}
      {experience && (
        <div style={{ marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#1e40af', 
            borderBottom: '3px solid #dbeafe',
            paddingBottom: '10px',
            fontSize: '22px'
          }}>
            💼 Experience
          </h2>
          <p style={{ fontSize: '16px', color: '#475569' }}>
            {experience}
          </p>
        </div>
      )}
      
      {/* Show education if available */}
      {education && (
        <div style={{ marginBottom: '25px' }}>
          <h2 style={{ 
            color: '#1e40af', 
            borderBottom: '3px solid #dbeafe',
            paddingBottom: '10px',
            fontSize: '22px'
          }}>
            🎓 Education
          </h2>
          <p style={{ fontSize: '16px', color: '#475569' }}>
            {education}
          </p>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalysis;
