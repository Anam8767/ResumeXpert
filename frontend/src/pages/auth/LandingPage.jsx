import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.scss";

const LandingPage = () => {
  const navigate = useNavigate();
  const [animate, setAnimate] = useState(false);
  const [typedText, setTypedText] = useState("");

  const heroText = "HireLens";
  const subText = "Gives recruiters a clearer lens and helps students know their preparation.";

  useEffect(() => {
    // Hero fade-in
    setTimeout(() => setAnimate(true), 200);

    // Typewriter effect for subText
    let index = 0;
    const interval = setInterval(() => {
      setTypedText(subText.slice(0, index + 1));
      index++;
      if (index === subText.length) clearInterval(interval);
    }, 30);
  }, []);

  return (
    <div className="landing-page">
      {/* Floating Shapes */}
      <div className="floating-shape shape1"></div>
      <div className="floating-shape shape2"></div>
      <div className="floating-shape shape3"></div>

      {/* Content */}
      <div className={`landing-content ${animate ? "animate" : ""}`}>
        <h1 className="hero-text">{heroText}</h1>
        <p className="sub-text">{typedText}</p>

        <div className="landing-buttons">
          <button
            className="cta-btn login-btn"
            onClick={() => navigate("/login")}
          >
            Login
          </button>
          <button
            className="cta-btn register-btn"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;