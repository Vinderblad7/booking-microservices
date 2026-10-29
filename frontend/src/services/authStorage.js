const ACCESS_TOKEN_KEY = 'access_token';

export function saveAccessToken(token) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function removeAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
}