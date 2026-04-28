import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api";

export default function Signup({ onSwitchToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("operator");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  async function handleSignup(e) {
    e.preventDefault();
    setErr("");
    setMsg("");

    try {
      await axios.post(`${API_BASE}/auth/signup`, {
        username,
        password,
        role,
      });

      setMsg("Account created successfully. You can now log in.");
    } catch (e) {
      setErr("Signup failed. Username may already exist.");
    }
  }

  return (
    <div style={{ maxWidth: "400px", margin: "80px auto", padding: "20px", background: "white" }}>
      <h2>Create Account</h2>

      <form onSubmit={handleSignup}>
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

        <div style={{ marginBottom: "10px" }}>
          <label>Role: </label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="operator">Operator</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button style={{ width: "100%", padding: "10px" }}>Sign Up</button>
      </form>

      {err && <p style={{ color: "red" }}>{err}</p>}
      {msg && <p style={{ color: "green" }}>{msg}</p>}

      <button onClick={onSwitchToLogin} style={{ marginTop: "10px", width: "100%" }}>
        Back to Login
      </button>
    </div>
  );
}