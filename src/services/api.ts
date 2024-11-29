import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const apiLogin = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
})

export const login = async (username: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await apiLogin.post('/login', formData);
  return response.data;
};

export interface Guest {
  id: number;
  name: string;
  contact: string;
  email: string;
  organization: string;
  location: string;
  guest_level: number;
  passport: string;
  nationality: string;
}

export const getGuests = async () => {
  const response = await api.get<Guest[]>('/guests/');
  return response.data;
};

// 添加嘉宾的API调用
export const addGuest = async (guest: Partial<Guest>) => {
  const response = await api.post<Guest>('/guests/', guest);
  return response.data;
};

// 删除嘉宾的API调用
export const deleteGuest = async (id: number) => {
  await api.delete(`/guests/${id}`);
};

// 更新嘉宾的API调用
export const updateGuest = async (id: number, guest: Partial<Guest>) => {
  const response = await api.put<Guest>(`/guests/${id}`, guest);
  return response.data;
};

// 设置认证token的拦截器
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
