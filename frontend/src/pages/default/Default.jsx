// import React from 'react'
// import Header from '../../layout/Header/Header'
// import { Outlet } from 'react-router-dom'

// const Default = () => {
//   return (
//     <>
//     <Header/>
//     <Outlet/>
//     </>
//   )
// }

// export default Default

import React from "react";
import Header from "../../layout/Header/Header";
import { Outlet } from "react-router-dom";
import "./Default.scss";

const Default = () => {
  return (
    <div className="app-layout">
      <Header />

      <main className="app-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Default;
