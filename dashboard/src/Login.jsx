import React, { useState } from "react";
import axios from "axios";
import { setToken } from "./api";
import Signup from "./Signup";

const API_BASE = "http://127.0.0.1:5000/api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [showSignup, setShowSignup] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setErr("");

    try {
      const res = await axios.post(`${API_BASE}/auth/login`, {
        username,
        password,
      });

      setToken(res.data.token);
      onLogin();
    } catch {
      setErr("Invalid credentials");
    }
  }

  if (showSignup) {
    return <Signup onSwitchToLogin={() => setShowSignup(false)} />;
  }

  return (
    <div style={{ maxWidth: "400px", margin: "80px auto", padding: "20px", background: "white" }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "10px" }}>
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: "10px" }}
          />
        </div>

        <div style={{ marginBottom: "10px" }}>
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "10px" }}
          />
        </div>

        <button style={{ width: "100%", padding: "10px" }}>Login</button>
      </form>

      {err && <p style={{ color: "red" }}>{err}</p>}

      <button onClick={() => setShowSignup(true)} style={{ marginTop: "10px", width: "100%" }}>
        Create New Account
      </button>
    </div>
  );
}