import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../utils/axios'; // Use the configured axios instance

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            console.log('Sending login request:', { email, password, role });
            const response = await axios.post('/auth/login', {
                email,
                password,
                role
            });

            console.log('Login response:', response.data);

            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('role', response.data.role);
                localStorage.setItem('user_id', response.data.user_id);

                console.log('Login successful, redirecting...', response.data.role);
                navigate(
                    response.data.role === 'Instructor'
                        ? '/instructor-dashboard'
                        : '/student-dashboard'
                );
            }
        } catch (error) {
            console.error('Login error:', error);
            setError(error.response?.data?.error || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    // You can return your JSX form here
    return (
        <form onSubmit={handleSubmit}>
            {/* Input fields for email, password, and role */}
            {/* Error and loading UI */}
        </form>
    );
};

export default Login;
