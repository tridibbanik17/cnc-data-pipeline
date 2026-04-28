import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api";

export default function App() {
  const [machines, setMachines] = useState([]);
  const [alarms, setAlarms] = useState([]);
  const [oee, setOee] = useState([]);

  async function loadData() {
    const m = await axios.get(`${API_BASE}/metrics/latest`);
    const a = await axios.get(`${API_BASE}/alarms`);
    const o = await axios.get(`${API_BASE}/oee`);

    setMachines(m.data);
    setAlarms(a.data);
    setOee(o.data);
  }

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      <h1>CNC Machine Dashboard</h1>
      <p>Real-time telemetry monitoring and KPI tracking</p>

      <h2>Latest Machine Status</h2>
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

      <h2>OEE (Estimated)</h2>
      <ul>
        {oee.map((x) => (
          <li key={x.machine_id}>
            {x.machine_id}: Availability={x.availability}, OEE={x.oee_estimate}
          </li>
        ))}
      </ul>

      <h2>Recent Alarms</h2>
      <ul>
        {alarms.map((a, i) => (
          <li key={i}>
            [{a.timestamp}] {a.machine_id} - {a.alarm_code}
          </li>
        ))}
      </ul>
    </div>
  );
}