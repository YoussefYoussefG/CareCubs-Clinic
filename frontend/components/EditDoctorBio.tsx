import React, { useState, useEffect } from 'react';
import { CircularProgress } from '@mui/material';

const EditDoctorBio = () => {
    const [bio, setBio] = useState('');
    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(true);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchBio = async () => {
            try {
                const doctorId = localStorage.getItem("userId");
                const token = localStorage.getItem("accessToken");
                const res = await fetch(`${process.env.NEXT_PUBLIC_SERVER_NAME}/get/doctor/${doctorId}?token=${token}`, {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });
                if (res.ok) {
                    const data = await res.json();
                    setBio(data.bio || '');
                }
            } catch (error) {
                console.error("Failed to fetch bio:", error);
            } finally {
                setFetching(false);
            }
        };
        fetchBio();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');
        try {
            const doctorId = localStorage.getItem("userId");
            const token = localStorage.getItem("accessToken");
            
            // First fetch the existing doctor to get all required fields for update
            const res = await fetch(`${process.env.NEXT_PUBLIC_SERVER_NAME}/get/doctor/${doctorId}?token=${token}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Failed to fetch current doctor data");
            const currentDoctor = await res.json();

            // Then send update request with bio included
            const updateRes = await fetch(`${process.env.NEXT_PUBLIC_SERVER_NAME}/update/doctor/${doctorId}?token=${token}`, {
                method: "PUT",
                headers: {
                    "Content-type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    userName: currentDoctor.userName,
                    email: currentDoctor.email,
                    password: "", // Handled by backend as unchanged if empty
                    firstName: currentDoctor.firstName,
                    lastName: currentDoctor.lastName,
                    profilePic: currentDoctor.profilePicture,
                    price: currentDoctor.price,
                    bio: bio
                }),
            });

            if (updateRes.ok) {
                setMessage("Bio updated successfully!");
            } else {
                setMessage("Failed to update bio.");
            }
        } catch (error) {
            console.error(error);
            setMessage("An error occurred.");
        } finally {
            setLoading(false);
        }
    };

    if (fetching) return <div className="flex justify-center p-4"><CircularProgress size="2rem" /></div>;

    return (
        <form onSubmit={handleSubmit} className="flex flex-col w-full h-full p-4 bg-white dark:bg-slate-900 rounded-xl">
            <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-200 mb-3">Your Public Brief / Bio</h3>
            <p className="text-sm text-slate-500 mb-4">
                This text will be displayed on the clinic's landing page. Let patients know about your expertise!
            </p>
            <textarea
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                className="w-full h-32 p-3 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:border-teal-500 resize-none dark:bg-slate-800 dark:text-white"
                placeholder="E.g., Expert pediatrician dedicated to your child's health..."
                required
            />
            <div className="flex items-center justify-between mt-4">
                <span className={`text-sm ${message.includes('success') ? 'text-green-500' : 'text-red-500'}`}>
                    {message}
                </span>
                <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-2 bg-teal-500 hover:bg-teal-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center min-w-[100px]"
                >
                    {loading ? <CircularProgress size="1rem" color="inherit" /> : 'Save Bio'}
                </button>
            </div>
        </form>
    );
};

export default EditDoctorBio;
