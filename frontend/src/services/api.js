import axios from "axios";
import mockOpportunities from "../mocks/opportunities.json";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === "true";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getHealth = async () => {
  if (USE_MOCKS) return { status: "healthy", database_connected: true };
  const res = await apiClient.get("/health");
  return res.data;
};

export const getProducts = async (params = {}) => {
  const res = await apiClient.get("/products", { params });
  return res.data;
};

export const getImportSummary = async () => {
  const res = await apiClient.get("/imports/summary");
  return res.data;
};

export const getOpportunities = async (params = {}) => {
  if (USE_MOCKS) {
    return mockOpportunities;
  }
  try {
    const res = await apiClient.get("/opportunities", { params });
    return res.data;
  } catch (err) {
    console.warn("Backend unavailable, falling back to mock opportunities:", err);
    return mockOpportunities;
  }
};

export const getRecommendations = async (targetUser = "farmer") => {
  const res = await apiClient.get("/recommendations", { params: { target_user: targetUser } });
  return res.data;
};

export default apiClient;
