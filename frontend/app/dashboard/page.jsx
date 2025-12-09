'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token) {
      router.push('/login');
      return;
    }

    // Redirect based on user role
    switch (user.role) {
      case 'seller':
        router.push('/seller/dashboard');
        break;
      case 'buyer':
        router.push('/catalog');
        break;
      case 'supplier':
        router.push('/supplier/dashboard'); // Future implementation
        break;
      default:
        router.push('/catalog');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-lg">Redirecting...</div>
    </div>
  );
}
