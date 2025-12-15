"use client";

import { useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "buyer",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const endpoint = isRegister ? "/auth/register" : "/auth/login";
      // NOTE: Adjust BASE_URL if your backend runs on a different host/port
      const baseUrl =
        process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

      const res = await fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: isRegister ? form.name : undefined,
          email: form.email,
          password: form.password,
          role: isRegister ? form.role : undefined,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Something went wrong");
      }

      const data = await res.json();

      if (!isRegister) {
        // Example: store token in localStorage; adjust to your real response shape
        if (data.access_token) {
          window.localStorage.setItem("access_token", data.access_token);
        }
        setSuccess("Logged in successfully.");
        // TODO: navigate to a protected page, e.g. dashboard
        // router.push("/dashboard");
      } else {
        setSuccess("Registered successfully. You can now log in.");
        setIsRegister(false);
      }
    } catch (err) {
      setError(err.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-zinc-200 to-indigo-200 text-zinc-900">
      <div className="mx-4 w-full max-w-md">
        <div className="w-full rounded-xl bg-white p-8 shadow-lg">
          <form onSubmit={handleSubmit} className="space-y-6">
            <h2 className="text-3xl font-semibold text-center">
              {isRegister ? "Register" : "Login"}
            </h2>

            {isRegister && (
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                required
                value={form.name}
                onChange={handleChange}
                className="w-full rounded-md border-0 bg-zinc-100 px-3 py-3 text-base text-zinc-900 outline-none"
              />
            )}

            <input
              type="email"
              name="email"
              placeholder="Email"
              required
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-md border-0 bg-zinc-100 px-3 py-3 text-base text-zinc-900 outline-none"
            />

            <input
              type="password"
              name="password"
              placeholder="Password"
              required
              value={form.password}
              onChange={handleChange}
              className="w-full rounded-md border-0 bg-zinc-100 px-3 py-3 text-base text-zinc-900 outline-none"
            />

            {isRegister && (
              <select
                name="role"
                required
                value={form.role}
                onChange={handleChange}
                className="w-full rounded-md border-0 bg-zinc-100 px-3 py-3 text-base text-zinc-900 outline-none"
              >
                <option value="">-- Select Role --</option>
                <option value="buyer">Buyer</option>
                <option value="admin">Admin</option>
              </select>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-md bg-fuchsia-500 px-3 py-3 text-base font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-60"
            >
              {loading
                ? isRegister
                  ? "Registering..."
                  : "Logging in..."
                : isRegister
                ? "Register"
                : "Login"}
            </button>

            {error && (
              <p className="text-center text-sm text-red-600">{error}</p>
            )}
            {success && (
              <p className="text-center text-sm text-emerald-600">{success}</p>
            )}

            <p className="text-center text-base">
              {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
              <button
                type="button"
                className="font-medium text-indigo-500 hover:underline"
                onClick={() => {
                  setIsRegister((prev) => !prev);
                  setError("");
                  setSuccess("");
                }}
              >
                {isRegister ? "Login" : "Register"}
              </button>
            </p>

            <p className="text-center text-sm text-zinc-500">
              <Link href="/">Back to home</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}


