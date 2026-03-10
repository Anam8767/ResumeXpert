import React from 'react';
import './ResumeAnalysis.css';

const ResumeAnalysis = ({ 
  score = 0, 
  skills = [], 
  suggestions = [], 
  fileName = 'Resume',
  experience = 'Not specified',
  education = 'Not specified'
}) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#059669'; // Green
    if (score >= 60) return '#d97706'; // Orange
    return '#dc2626'; // Red
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    return 'Needs Improvement';
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
        background: score >= 80 ? '#ecfdf5' : score >= 60 ? '#fffbeb' : '#fef2f2',
        padding: '15px',
        borderRadius: '10px',
        marginBottom: '20px'
      }}>
        {score > 0 ? `${score}% Job Match Score` : 'No Analysis Yet'}
      </div>

      {score > 0 && (
        <>
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
              {skills.length > 0 ? (
                skills.map((skill, index) => (
                  <span key={index} style={{
                    background: '#eff6ff',
                    color: '#1e40af',
                    padding: '8px 16px',
                    borderRadius: '25px',
                    fontWeight: 'bold',
                    fontSize: '14px'
                  }}>
                    {typeof skill === 'string' ? skill : skill.name || skill}
                  </span>
                ))
              ) : (
                <p style={{ color: '#6b7280', fontStyle: 'italic' }}>
                  No specific skills identified yet. Upload and analyze your resume to see skills.
                </p>
              )}
            </div>
          </div>

          {suggestions.length > 0 && (
            <div style={{ marginBottom: '25px' }}>
              <h2 style={{ 
                color: '#1e40af', 
                borderBottom: '3px solid #dbeafe',
                paddingBottom: '10px',
                fontSize: '22px'
              }}>
                💡 Top Suggestions
              </h2>
              <ul style={{ lineHeight: '1.6', paddingLeft: '20px' }}>
                {suggestions.map((suggestion, index) => (
                  <li key={index} style={{ marginBottom: '8px' }}>
                    {typeof suggestion === 'string' ? suggestion : suggestion.text || suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div style={{ marginBottom: '25px' }}>
            <h2 style={{ 
              color: '#1e40af', 
              borderBottom: '3px solid #dbeafe',
              paddingBottom: '10px',
              fontSize: '22px'
            }}>
              📊 Analysis Summary
            </h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '15px',
              marginTop: '15px'
            }}>
              <div style={{
                background: '#f8fafc',
                padding: '15px',
                borderRadius: '8px',
                border: '1px solid #e2e8f0'
              }}>
                <div style={{ fontWeight: 'bold', color: '#475569', marginBottom: '5px' }}>
                  Overall Rating
                </div>
                <div style={{ fontSize: '18px', color: getScoreColor(score) }}>
                  {getScoreLabel(score)}
                </div>
              </div>
              
              <div style={{
                background: '#f8fafc',
                padding: '15px',
                borderRadius: '8px',
                border: '1px solid #e2e8f0'
              }}>
                <div style={{ fontWeight: 'bold', color: '#475569', marginBottom: '5px' }}>
                  Experience Level
                </div>
                <div style={{ fontSize: '16px', color: '#1e293b' }}>
                  {experience}
                </div>
              </div>
              
              <div style={{
                background: '#f8fafc',
                padding: '15px',
                borderRadius: '8px',
                border: '1px solid #e2e8f0'
              }}>
                <div style={{ fontWeight: 'bold', color: '#475569', marginBottom: '5px' }}>
                  Education
                </div>
                <div style={{ fontSize: '16px', color: '#1e293b' }}>
                  {education}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {score === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#6b7280'
        }}>
          <div style={{ fontSize: '48px', marginBottom: '20px' }}>📄</div>
          <h3>No Analysis Available</h3>
          <p>Upload your resume and ask me to analyze it to see detailed insights.</p>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalysis;
