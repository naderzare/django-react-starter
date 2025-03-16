import axios from '../axiosConfig';
import { PaymentTransaction } from '../types/auth';

export const paymentService = {
    getUserAccount: async () => {
        const response = await axios.get('/api/account/');
        return response.data;
    },
    
    createPayment: async (productId: string) => {
        // No need to pass amount from front-end if your back-end enforces it
        const response = await axios.post('/api/payments/create/', {
            product_id: productId
        });
        return response.data;
    },
    
    getPaymentHistory: async () => {
        const response = await axios.get<PaymentTransaction[]>('/api/payments/history/');
        return response.data;
    },

    getProducts: async () => {
        const response = await axios.get('/api/payments/products/');
        return response.data;  // an array of products
    }
};
