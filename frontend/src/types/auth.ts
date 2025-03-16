export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    account_value?: number;
}

export interface LoginResponse {
    access: string;
    refresh: string;
    user: User;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterCredentials {
    username: string;
    email: string;
    password1: string;
    password2: string;
}

export interface PaymentTransaction {
    id: number;
    transaction_id: string;
    amount: number;
    currency: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    payment_method: string;
    created_at: string;
}

export interface PaymentProduct {
    id: string;
    name: string;
    description: string;
    price: number;
    currency: string;
    credits: number;
}