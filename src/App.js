import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";

const DashboardRedirect = () => {
    window.location.href = "http://127.0.0.1:5000"; // Redirect to Flask dashboard
    return null;
};

function App() {
    const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={isAuthenticated ? <DashboardRedirect /> : <Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;
