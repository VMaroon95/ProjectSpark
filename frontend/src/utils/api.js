const API_BASE = window.location.port === '3000' ? 'http://localhost:8000' : '';

window.api = {
    async getHealth() {
        const res = await fetch(`${API_BASE}/api/health`);
        return res.json();
    },
    async getEvalResults() {
        const res = await fetch(`${API_BASE}/api/eval/results`);
        return res.json();
    },
    async getHeatmap() {
        const res = await fetch(`${API_BASE}/api/eval/heatmap`);
        return res.json();
    },
    async uploadEvalResults(file) {
        const fd = new FormData();
        fd.append('file', file);
        const res = await fetch(`${API_BASE}/api/eval/upload`, { method: 'POST', body: fd });
        return res.json();
    },
    async runAudit(file) {
        const fd = new FormData();
        fd.append('file', file);
        const res = await fetch(`${API_BASE}/api/compliance/audit`, { method: 'POST', body: fd });
        return res.json();
    },
    async getAudit(auditId) {
        const res = await fetch(`${API_BASE}/api/compliance/audit/${auditId}`);
        return res.json();
    },
    async generatePDF(formData) {
        const res = await fetch(`${API_BASE}/api/compliance/disclosure-pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });
        return res.blob();
    },
    async getStats() {
        const res = await fetch(`${API_BASE}/api/stats`);
        return res.json();
    },
};
