import React from "react";

function Sidebar() {

  return (
    <aside className="sidebar">

      <div className="logo">
        <div className="logo-icon">🚀</div>

        <div>
          <h2>DataProof</h2>
          <span>AI</span>
        </div>
      </div>


      <div className="menu">

        <p className="menu-title">MAIN</p>

        <a href="#" className="menu-item active">
          <span>◈</span>
          Dashboard
        </a>

        <a href="#" className="menu-item">
          <span>📁</span>
          Datasets
        </a>

        <a href="#" className="menu-item">
          <span>📊</span>
          Analytics
        </a>

        <a href="#" className="menu-item">
          <span>🕘</span>
          History
        </a>


        <p className="menu-title settings-title">
          SYSTEM
        </p>

        <a href="#" className="menu-item">
          <span>⚙️</span>
          Settings
        </a>

      </div>


      <div className="sidebar-bottom">

        <div className="help-box">
          <div className="help-icon">?</div>

          <div>
            <strong>Need help?</strong>
            <p>Ask DataProof AI</p>
          </div>
        </div>

      </div>

    </aside>
  );
}

export default Sidebar;