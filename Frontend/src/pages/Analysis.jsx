import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

export default function Analysis() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()
    const location = useLocation()

    const [resumes, setResumes] = useState([])
    const [selectedResume, setSelectedResume] = useState('')
    const [jobDescription, setJobDescription] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState('')

    // If user clicked "Analyze" from resume page, auto-select that resume
    useEffect(() => {
        fetchResumes()
        if (location.state?.resumeId) {
            setSelectedResume(String(location.state.resumeId))
        }
    }, [])

    const fetchResumes = async () => {
        try {
            const res = await api.get('/resume/')
            setResumes(res.data)
        } catch (err) {
            setError('Failed to load resumes.')
        }
    }

    const handleAnalyze = async () => {
        if (!selectedResume) {
            setError('Please select a resume.')
            return
        }
        if (!jobDescription.trim()) {
            setError('Please paste a job description.')
            return
        }
        if (jobDescription.trim().length < 50) {
            setError('Job description is too short. Paste the full job posting.')
            return
        }

        setError('')
        setResult(null)
        setLoading(true)

        try {
            const res = await api.post('/analysis/run', {
                resume_id: parseInt(selectedResume),
                job_description: jobDescription,
            })
            setResult(res.data)
        } catch (err) {
            if (err.response?.status === 429) {
                setError('You have reached your free analysis limit.')
            } else {
                setError(err.response?.data?.detail || 'Analysis failed. Try again.')
            }
        } finally {
            setLoading(false)
        }
    }

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    // Determine score color
    const getScoreColor = (score) => {
        if (score >= 75) return 'text-green-600'
        if (score >= 50) return 'text-yellow-500'
        return 'text-red-500'
    }

    const getScoreBg = (score) => {
        if (score >= 75) return 'bg-green-50 border-green-200'
        if (score >= 50) return 'bg-yellow-50 border-yellow-200'
        return 'bg-red-50 border-red-200'
    }

    const getScoreLabel = (score) => {
        if (score >= 75) return 'Strong Match 🎉'
        if (score >= 50) return 'Moderate Match ⚠️'
        return 'Weak Match ❌'
    }

    return (
        <div className="min-h-screen bg-gray-50">

            {/* Navbar */}
            <nav className="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow">
                <h1
                    className="text-xl font-bold cursor-pointer"
                    onClick={() => navigate('/dashboard')}
                >
                    CareerLens AI
                </h1>
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="text-sm text-blue-200 hover:text-white transition"
                    >
                        Dashboard
                    </button>
                    <button
                        onClick={() => navigate('/resume')}
                        className="text-sm text-blue-200 hover:text-white transition"
                    >
                        Resumes
                    </button>
                    <span className="text-sm text-blue-200">|</span>
                    <span className="text-sm text-blue-200">{user?.full_name}</span>
                    <button
                        onClick={handleLogout}
                        className="bg-blue-700 hover:bg-blue-600 text-sm px-4 py-2 rounded-lg transition"
                    >
                        Logout
                    </button>
                </div>
            </nav>

            <main className="max-w-3xl mx-auto px-6 py-12">
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-blue-900">AI Resume Analysis</h2>
                    <p className="text-gray-500 mt-1">
                        Select your resume, paste a job description, and get your match score instantly.
                    </p>
                </div>

                {/* Usage warning */}
                {user && user.analyses_used >= user.free_limit && (
                    <div className="bg-orange-50 border border-orange-200 text-orange-700 px-4 py-3 rounded-lg mb-6 text-sm font-medium">
                        You have used all {user.free_limit} free analyses.
                    </div>
                )}

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
                        {error}
                    </div>
                )}

                {/* Input Form */}
                <div className="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-8 space-y-6">

                    {/* Resume Selector */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            Select Resume
                        </label>
                        {resumes.length === 0 ? (
                            <div className="text-sm text-gray-400 bg-gray-50 rounded-lg px-4 py-3 border border-gray-200">
                                No resumes uploaded yet.{' '}
                                <span
                                    onClick={() => navigate('/resume')}
                                    className="text-blue-600 cursor-pointer hover:underline font-medium"
                                >
                                    Upload one first →
                                </span>
                            </div>
                        ) : (
                            <select
                                value={selectedResume}
                                onChange={(e) => setSelectedResume(e.target.value)}
                                className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">-- Choose a resume --</option>
                                {resumes.map((r) => (
                                    <option key={r.id} value={r.id}>
                                        {r.filename}
                                    </option>
                                ))}
                            </select>
                        )}
                    </div>

                    {/* Job Description */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            Job Description
                        </label>
                        <textarea
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            rows={10}
                            placeholder="Paste the full job description here...

Example:
We are looking for a React Developer with 2+ years of experience.
Skills required: React, TypeScript, REST APIs, Git..."
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                        />
                        <p className="text-xs text-gray-400 mt-1">
                            {jobDescription.length} characters — paste the full job posting for best results
                        </p>
                    </div>

                    {/* Analyze Button */}
                    <button
                        onClick={handleAnalyze}
                        disabled={loading || !selectedResume || !jobDescription.trim()}
                        className="w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                Analyzing with AI...
                            </span>
                        ) : (
                            '🧠 Analyze Resume'
                        )}
                    </button>
                </div>

                {/* Results Section */}
                {result && (
                    <div className="space-y-6">

                        {/* Score Card */}
                        <div className={`rounded-2xl border p-8 text-center ${getScoreBg(result.match_score)}`}>
                            <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                                Match Score
                            </p>
                            <p className={`text-7xl font-black mb-2 ${getScoreColor(result.match_score)}`}>
                                {Math.round(result.match_score)}%
                            </p>
                            <p className={`text-lg font-semibold ${getScoreColor(result.match_score)}`}>
                                {getScoreLabel(result.match_score)}
                            </p>

                            {/* Score bar */}
                            <div className="mt-6 bg-white rounded-full h-3 max-w-xs mx-auto">
                                <div
                                    className={`h-3 rounded-full transition-all ${result.match_score >= 75
                                            ? 'bg-green-500'
                                            : result.match_score >= 50
                                                ? 'bg-yellow-400'
                                                : 'bg-red-500'
                                        }`}
                                    style={{ width: result.match_score + "%" }}
                                />
                            </div>
                        </div>

                        {/* Missing Keywords */}
                        {result.missing_keywords && result.missing_keywords.length > 0 && (
                            <div className="bg-white rounded-2xl border border-gray-100 shadow p-6">
                                <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    <span>🔍</span> Missing Keywords
                                </h3>
                                <p className="text-sm text-gray-500 mb-4">
                                    These important keywords from the job description are missing from your resume:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {result.missing_keywords.map((keyword, i) => (
                                        <span
                                            key={i}
                                            className="bg-red-50 text-red-700 border border-red-200 text-xs font-semibold px-3 py-1.5 rounded-full"
                                        >
                                            {keyword}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Suggestions */}
                        {result.suggestions && result.suggestions.length > 0 && (
                            <div className="bg-white rounded-2xl border border-gray-100 shadow p-6">
                                <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    <span>💡</span> AI Suggestions
                                </h3>
                                <p className="text-sm text-gray-500 mb-4">
                                    Here is how to improve your resume for this role:
                                </p>
                                <div className="space-y-3">
                                    {result.suggestions.map((suggestion, i) => (
                                        <div
                                            key={i}
                                            className="flex gap-3 bg-blue-50 border border-blue-100 rounded-xl px-4 py-3"
                                        >
                                            <span className="text-blue-600 font-bold text-sm mt-0.5">
                                                {i + 1}.
                                            </span>
                                            <p className="text-sm text-gray-700">{suggestion}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Full AI Feedback */}
                        {result.ai_feedback && (
                            <div className="bg-white rounded-2xl border border-gray-100 shadow p-6">
                                <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    <span>🤖</span> Full AI Response
                                </h3>
                                <pre className="text-xs text-gray-500 bg-gray-50 rounded-lg p-4 overflow-auto whitespace-pre-wrap">
                                    {result.ai_feedback}
                                </pre>
                            </div>
                        )}

                        {/* Analyze Again */}
                        <button
                            onClick={() => setResult(null)}
                            className="w-full border border-blue-300 text-blue-700 font-semibold py-3 rounded-lg hover:bg-blue-50 transition"
                        >
                            Run Another Analysis
                        </button>
                    </div>
                )}
            </main>
        </div>
    )
}