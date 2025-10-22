import axios from "axios";
const API_URL = "http://localhost:8000/api";

export const scoreTransaction = async (tx) => {
  const response = await axios.post(`${API_URL}/score`, tx);
  return response.data;
};

export const getAlerts = async () => {
  const response = await axios.get(`${API_URL}/alerts`);
  // return array of alerts or [] if keys differ
  return response.data.alerts || [];
};
