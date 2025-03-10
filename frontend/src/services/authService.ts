import axios from '../axiosConfig';
import { LoginCredentials, LoginResponse, RegisterCredentials } from '../types/auth';

export const authService = {
    login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
        const response = await axios.post('/auth/login/', credentials);
        return response.data;
    },

    register: async (credentials: RegisterCredentials): Promise<LoginResponse> => {
        const response = await axios.post('/auth/registration/', credentials);
        return response.data;
    },

    googleLogin: async (token: string): Promise<LoginResponse> => {
        const response = await axios.post('/api/auth/google/', { token });
        return response.data;
    },

    logout: async (): Promise<void> => {
        await axios.post('/auth/logout/');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }
};