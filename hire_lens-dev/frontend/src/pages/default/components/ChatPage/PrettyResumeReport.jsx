import React from 'react';
import './ResumeAnalysis.css';

const ResumeAnalysis = () => {
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
        color: '#059669',
        background: '#ecfdf5',
        padding: '15px',
        borderRadius: '10px',
        marginBottom: '20px'
      }}>
        92% Job Match Score
      </div>
      
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
          <span style={{
            background: '#eff6ff',
            color: '#1e40af',
            padding: '8px 16px',
            borderRadius: '25px',
            fontWeight: 'bold',
            fontSize: '14px'
          }}>HTML</span>
          <span style={{
            background: '#eff6ff',
            color: '#1e40af',
            padding: '8px 16px',
            borderRadius: '25px',
            fontWeight: 'bold',
            fontSize: '14px'
          }}>CSS</span>
          <span style={{
            background: '#eff6ff',
            color: '#1e40af',
            padding: '8px 16px',
            borderRadius: '25px',
            fontWeight: 'bold',
            fontSize: '14px'
          }}>JavaScript</span>
          <span style={{
            background: '#eff6ff',
            color: '#1e40af',
            padding: '8px 16px',
            borderRadius: '25px',
            fontWeight: 'bold',
            fontSize: '14px'
          }}>Salesforce</span>
        </div>
      </div>
      
      <div style={{ marginBottom: '25px' }}>
        <h2 style={{ 
          color: '#1e40af', 
          borderBottom: '3px solid #dbeafe',
          paddingBottom: '10px',
          fontSize: '22px'
        }}>
          💼 Strengths
        </h2>
        <ul style={{ lineHeight: '1.6', paddingLeft: '20px' }}>
          <li>Strong match on core technical skills</li>
          <li>Relevant project experience in web development</li>
          <li>Salesforce Resume Management System expertise</li>
        </ul>
      </div>
    </div>
  );
};

export default ResumeAnalysis;
