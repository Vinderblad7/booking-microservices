import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home";
import Register from "./pages/Register/Register";
import Login from "./pages/Login/Login";
import Header from "./components/Header/Header";
import Hotels from "./pages/Hotels/Hotels"

function App() {  
  return (
    <>
      <Header />
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/hotels" element={<Hotels />} />
      </Routes>
    </>
  );
}

export default App;