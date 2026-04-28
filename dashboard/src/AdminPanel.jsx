import React, { useEffect, useState } from "react";
import { api } from "./api";

export default function AdminPanel() {
  const [users, setUsers] = useState([]);

  async function loadUsers() {
    const res = await api.get("/admin/users");
    setUsers(res.data);
  }

  async function updateRole(userId, role) {
    await api.put(`/admin/users/${userId}/role`, { role });
    loadUsers();
  }

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <div style={{ background: "white", padding: "15px", marginBottom: "20px" }}>
      <h2>Admin Panel: User Management</h2>

      <table border="1" cellPadding="8" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Role</th>
            <th>Set Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.role}</td>
              <td>
                <button onClick={() => updateRole(u.id, "operator")}>Operator</button>{" "}
                <button onClick={() => updateRole(u.id, "admin")}>Admin</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}