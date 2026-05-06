import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

export default function Resume() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const [resumes, setResumes] = useState([])
  const [uploading, setUploading] = useState(false)
  const [deleting, setDeleting] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [dragOver, setDragOver] = useState(false)

  // Fetch all resumes when page loads
  useEffect(() => {
    fetchResumes()
  }, [])

  const fetchResumes = async () => {
    try {
      const res = await api.get('/resume/')
      setResumes(res.data)
    } catch (err) {
      setError('Failed to load resumes.')
    }
  }

  const handleFileUpload = async (file) => {
    // Only allow PDFs
    if (!file || !file.name.endsWith('.pdf')) {
      setError('Only PDF files are accepted.')
      return
    }

    setError('')
    setSuccess('')
    setUploading(true)

    try {
      // File uploads need FormData — not JSON
      // This is different from all other API calls
      const formData = new FormData()
      formData.append('file', file)

      await api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      setSuccess('Resume uploaded successfully!')
      fetchResumes()  // refresh the list
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Try again.')
    } finally {
      setUploading(false)
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) handleFileUpload(file)
  }

  // Drag and drop handlers
  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = () => setDragOver(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFileUpload(file)
  }

  const handleDelete = async (resumeId) => {
    setDeleting(resumeId)
    try {
      await api.delete(`/resume/${resumeId}`)
      setResumes(resumes.filter(r => r.id !== resumeId))
      setSuccess('Resume deleted.')
    } catch (err) {
      setError('Failed to delete resume.')
    } finally {
      setDeleting(null)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric'
    })
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
            onClick={() => navigate('/analysis')}
            className="text-sm text-blue-200 hover:text-white transition"
          >
            Analyze
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
          <h2 className="text-2xl font-bold text-blue-900">My Resumes</h2>
          <p className="text-gray-500 mt-1">Upload your PDF resume to use in AI analysis</p>
        </div>

        {/* Success / Error messages */}
        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6 text-sm">
            {success}
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        {/* Upload Area */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-2xl p-12 text-center mb-8 transition-all ${
            dragOver
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 bg-white hover:border-blue-400'
          }`}
        >
          {uploading ? (
            <div className="flex flex-col items-center gap-3">
              <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <p className="text-gray-500 text-sm">Uploading and extracting text...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="text-5xl">📄</div>
              <p className="text-gray-700 font-medium">
                Drag and drop your PDF here
              </p>
              <p className="text-gray-400 text-sm">or</p>
              <label className="cursor-pointer bg-blue-700 hover:bg-blue-800 text-white text-sm font-semibold px-6 py-3 rounded-lg transition">
                Browse File
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
              <p className="text-gray-400 text-xs mt-1">PDF files only</p>
            </div>
          )}
        </div>

        {/* Resume List */}
        <div>
          <h3 className="font-semibold text-gray-700 mb-4">
            Uploaded Resumes ({resumes.length})
          </h3>

          {resumes.length === 0 ? (
            <div className="bg-white rounded-2xl border border-gray-100 shadow p-8 text-center">
              <p className="text-gray-400 text-sm">No resumes uploaded yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {resumes.map((resume) => (
                <div
                  key={resume.id}
                  className="bg-white rounded-xl border border-gray-100 shadow-sm px-5 py-4 flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">📄</span>
                    <div>
                      <p className="font-medium text-gray-800 text-sm">{resume.filename}</p>
                      <p className="text-xs text-gray-400 mt-0.5">
                        Uploaded {formatDate(resume.created_at)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => navigate('/analysis', { state: { resumeId: resume.id } })}
                      className="bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-semibold px-4 py-2 rounded-lg transition"
                    >
                      Analyze
                    </button>
                    <button
                      onClick={() => handleDelete(resume.id)}
                      disabled={deleting === resume.id}
                      className="bg-red-50 hover:bg-red-100 text-red-600 text-xs font-semibold px-4 py-2 rounded-lg transition disabled:opacity-50"
                    >
                      {deleting === resume.id ? 'Deleting...' : 'Delete'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}