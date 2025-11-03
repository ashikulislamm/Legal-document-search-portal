import axios from "axios";

const API_BASE =
  import.meta.env.VITE_API?.replace(/\/+$/, "") || "http://localhost:8000";

export async function generate(query) {
  const { data } = await axios.post(
    `${API_BASE}/generate`,
    { query },
    { headers: { "Content-Type": "application/json" } }
  );
  return data;
}
