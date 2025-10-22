import React from "react";

export default function Navbar({ user }) {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between">
      <div className="font-bold text-xl">AI AML Platform</div>
      <div>{user ? `Logged in as ${user}` : "Guest"}</div>
    </nav>
  );
}
