import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/dashboard";

function App() {
  const [user, setUser] = useState(null);

  return (
    <div>
      <Navbar user={user} />
      {!user ? <Login onLogin={setUser} /> : <Dashboard />}
    </div>
  );
}

export default App;
