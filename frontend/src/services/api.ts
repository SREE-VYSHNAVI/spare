import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const fetchDashboardSummary = async () => {
    const response = await axios.get(`${API_BASE_URL}/dashboard`);
    return response.data;
};

export const fetchInventoryStatus = async () => {
    const response = await axios.get(`${API_BASE_URL}/inventory`);
    return response.data;
};

export const sendAIChatQuery = async (query: string) => {
    const response = await axios.post(`${API_BASE_URL}/ai/query`, { query });
    return response.data.response;
};

export const predictMachineFailure = async (sensors: {
    vibration_mm_s: number;
    bearing_temp_c: number;
    motor_current_a: number;
    pressure_bar: number;
}) => {
    const response = await axios.post(`${API_BASE_URL}/predict/failure`, sensors);
    return response.data;
};