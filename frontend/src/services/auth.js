import { getAccessToken } from "./authStorage";

const AUTH_API_URL = 'http://localhost:8001/api/auth';

export async function registerUser({ email, password }) {
    const response = await fetch(`${AUTH_API_URL}/register`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email.trim(),
            password,
        }),
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const error = new Error(
            data?.detail || 'Не удалось создать аккаунт'
        );

        error.status = response.status;
        throw error;
    }
    
    return data;
}

export async function loginUser({ email, password }) {
    const response = await fetch(`${AUTH_API_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email.trim(),
            password,
        }),
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const error = new Error(
            data?.detail || 'Не удалось войти в аккаунт'
        );

        error.status = response.status;
        throw error;
    }

    return data;
}

export async function getCurrentUser() {
    const token = getAccessToken();

    const response = await fetch(`${AUTH_API_URL}/me`, {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const error = new Error(
            data?.detail || 'Не удалось получить пользователя'
        );

        error.status = response.status;
        throw error;
    }

    return data;
}