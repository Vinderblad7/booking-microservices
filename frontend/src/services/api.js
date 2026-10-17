const API_URL = 'http://127.0.0.1:8000/api';

export async function getHotels() {
    const response = await fetch(`${API_URL}/hotels`);

    if (!response.ok) {
        throw new Error('Failed to fetch hotels');
    }

    return await response.json();
}
