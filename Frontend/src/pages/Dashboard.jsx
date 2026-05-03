import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    const usagePercent = user ? (user.analyses_used / user.free_limit) * 100 : 0

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow">
                <h1 className="text-xl font-bold">CareerLens AI</h1>
                <div className="flex items-center gap-4">
                    <span className="text-sm text-blue-200">Hello, {user?.full_name}</span>
                    <button
                        onClick={handleLogout}
                        className="bg-blue-700 hover:bg-blue-600 text-sm px-4 py-2 rounded-lg transition"
                    >
                        Logout
                    </button>
                </div>
            </nav>

            <main className="max-w-4xl mx-auto px-6 py-12">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-blue-900">
                        Welcome back, {user?.full_name?.split(' ')[0]}
                    </h2>
                    <p className="text-gray-500 mt-2">
                        Upload your resume and paste a job description to get your AI match score.
                    </p>
                </div>

                <div className="bg-white rounded-2xl shadow p-6 mb-8 border border-gray-100">
                    <h3 className="font-semibold text-gray-700 mb-3">Free Plan Usage</h3>
                    <div className="flex items-center gap-4">
                        <div className="flex-1 bg-gray-200 rounded-full h-3">
                            <div
                                className="bg-blue-600 h-3 rounded-full transition-all"
                                style={{ width: usagePercent + "%" }}
                            />
                        </div>
                        <span className="text-sm text-gray-600 font-medium">
                            {user?.analyses_used} / {user?.free_limit} analyses used
                        </span>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white rounded-2xl shadow p-6 border border-gray-100 opacity-60">
                        <div className="text-3xl mb-3">📄</div>
                        <h3 className="font-semibold text-gray-800 mb-1">Upload Resume</h3>
                        <p className="text-sm text-gray-500">Upload your PDF resume to get started</p>
                        <span className="text-xs text-blue-600 font-medium mt-3 inline-block">Coming next</span>
                    </div>

                    <div className="bg-white rounded-2xl shadow p-6 border border-gray-100 opacity-60">
                        <div className="text-3xl mb-3">🧠</div>
                        <h3 className="font-semibold text-gray-800 mb-1">AI Analysis</h3>
                        <p className="text-sm text-gray-500">Paste a job description and get your match score</p>
                        <span className="text-xs text-blue-600 font-medium mt-3 inline-block">Coming next</span>
                    </div>
                </div>
            </main>
        </div>
    )
}