import React, { useEffect, useState } from "react";
import { api, getToken, logout } from "./api";
import Login from "./Login";
import "./App.css";

import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

export default function App() {
  const [machines, setMachines] = useState([]);
  const [alarms, setAlarms] = useState([]);
  const [oee, setOee] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [downtime, setDowntime] = useState([]);

  const [loggedIn, setLoggedIn] = useState(!!getToken());

  async function loadData() {
    const m = await api.get("/metrics/latest");
    const a = await api.get("/alarms");
    const o = await api.get("/oee");
    const an = await api.get("/anomalies");
    const d = await api.get("/downtime");

    setMachines(m.data);
    setAlarms(a.data);
    setOee(o.data);
    setAnomalies(an.data);
    setDowntime(d.data);
  }

  useEffect(() => {
    if (!loggedIn) return;

    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, [loggedIn]);

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  const oeeChartData = oee.map((x) => ({
    machine: x.machine_id,
    availability: x.availability,
    oee: x.oee_estimate,
  }));

  const anomalyChartData = anomalies.slice(0, 20).map((x) => ({
    machine: x.machine_id,
    severity: x.severity,
    time: x.timestamp.substring(11, 19),
  }));

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>CNC Industry 4.0 Dashboard</h1>
        <button
          onClick={() => {
            logout();
            setLoggedIn(false);
          }}
        >
          Logout
        </button>
      </div>

      <p style={{ color: "#444" }}>
        Real-time telemetry ingestion, OEE analytics, alarms, anomaly detection, and downtime tracking.
      </p>

      {/* MACHINE TABLE */}
      <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
        <h2>Live Machine Status</h2>
        <table border="1" cellPadding="8" style={{ width: "100%" }}>
          <thead>
            <tr>
              <th>Machine</th>
              <th>Timestamp</th>
              <th>Spindle Load</th>
              <th>Tool Wear</th>
              <th>Cycle Time</th>
              <th>Uptime</th>
              <th>Alarm</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((m) => (
              <tr key={m.machine_id}>
                <td>{m.machine_id}</td>
                <td>{m.timestamp}</td>
                <td>{m.spindle_load}</td>
                <td>{m.tool_wear}</td>
                <td>{m.cycle_time}</td>
                <td>{m.uptime ? "YES" : "NO"}</td>
                <td>{m.alarm_active ? m.alarm_code : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* OEE CHART */}
      <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
        <h2>OEE & Availability (Estimated)</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={oeeChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="machine" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="availability" />
            <Bar dataKey="oee" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ANOMALY CHART */}
      <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
        <h2>Recent Anomaly Severity</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={anomalyChartData}>
            <Line type="monotone" dataKey="severity" strokeWidth={2} />
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* RECENT ALARMS */}
      <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
        <h2>Recent Alarms</h2>
        <ul>
          {alarms.map((a, i) => (
            <li key={i}>
              [{a.timestamp}] {a.machine_id} - {a.alarm_code}
            </li>
          ))}
        </ul>
      </div>

      {/* DOWNTIME */}
      <div style={{ background: "white", padding: "15px" }}>
        <h2>Downtime Events</h2>
        <ul>
          {downtime.map((d, i) => (
            <li key={i}>
              {d.machine_id} | Start: {d.start_time} | End: {d.end_time || "ONGOING"} | Reason: {d.reason}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}