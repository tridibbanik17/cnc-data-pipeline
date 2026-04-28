import React, { useEffect, useState } from "react";
import { api } from "./api";

import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function MachineDetails({ machineId }) {
  const [data, setData] = useState([]);

  async function loadHistory() {
    const res = await api.get(`/machines/${machineId}/history?limit=100`);
    const points = res.data.points.map((p) => ({
      time: p.timestamp.substring(11, 19),
      spindle_load: p.spindle_load,
      tool_wear: p.tool_wear,
      cycle_time: p.cycle_time,
    }));
    setData(points);
  }

  useEffect(() => {
    if (!machineId) return;
    loadHistory();
    const interval = setInterval(loadHistory, 4000);
    return () => clearInterval(interval);
  }, [machineId]);

  if (!machineId) return null;

  return (
    <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
      <h2>Machine History: {machineId}</h2>

      <h3>Spindle Load Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line type="monotone" dataKey="spindle_load" strokeWidth={2} />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
        </LineChart>
      </ResponsiveContainer>

      <h3>Cycle Time Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line type="monotone" dataKey="cycle_time" strokeWidth={2} />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
        </LineChart>
      </ResponsiveContainer>

      <h3>Tool Wear Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line type="monotone" dataKey="tool_wear" strokeWidth={2} />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}