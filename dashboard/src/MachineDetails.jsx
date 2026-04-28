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

      {/* ---------------- Spindle Load ---------------- */}
      <h3>Spindle Load Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line
            type="monotone"
            dataKey="spindle_load"
            strokeWidth={2}
            name="Spindle Load (%)"
            stroke="#0077cc"
          />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis
            label={{
              value: "Spindle Load (%)",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip formatter={(v) => `${v}%`} />
        </LineChart>
      </ResponsiveContainer>

      {/* ---------------- Cycle Time ---------------- */}
      <h3>Cycle Time Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line
            type="monotone"
            dataKey="cycle_time"
            strokeWidth={2}
            name="Cycle Time (s)"
            stroke="#cc5500"
          />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis
            label={{
              value: "Cycle Time (s)",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip formatter={(v) => `${v}s`} />
        </LineChart>
      </ResponsiveContainer>

      {/* ---------------- Tool Wear ---------------- */}
      <h3>Tool Wear Trend</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <Line
            type="monotone"
            dataKey="tool_wear"
            strokeWidth={2}
            name="Tool Wear (mm)"
            stroke="#22aa44"
          />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis
            label={{
              value: "Tool Wear (mm)",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip formatter={(v) => `${v} mm`} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}