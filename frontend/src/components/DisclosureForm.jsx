function DisclosureForm() {
    const [form, setForm] = React.useState({
        organization_name: '', model_name: '', date: new Date().toISOString().slice(0, 10),
        contact_name: '', contact_email: '', audit_id: '',
    });
    const [generating, setGenerating] = React.useState(false);

    const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

    const handleGenerate = async () => {
        if (!form.organization_name || !form.model_name) {
            alert('Please fill in Organization Name and Model Name.');
            return;
        }
        setGenerating(true);
        try {
            const blob = await api.generatePDF(form);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'CLEAR_Act_Disclosure_Form.pdf';
            a.click();
            URL.revokeObjectURL(url);
        } catch (e) {
            alert('Error generating PDF: ' + e.message);
        }
        setGenerating(false);
    };

    const field = (label, key, type) =>
        React.createElement('div', { className: 'form-field' },
            React.createElement('label', null, label),
            React.createElement('input', { type: type || 'text', value: form[key], onChange: update(key) }),
        );

    return React.createElement('div', { className: 'disclosure-form' },
        React.createElement('h2', null, 'Federal Disclosure Form Generator'),
        React.createElement('p', { className: 'subtitle' }, 'Generate a CLEAR Act compliance PDF for regulatory filing.'),
        React.createElement('div', { className: 'card form-card' },
            React.createElement('div', { className: 'form-grid' },
                field('Organization Name *', 'organization_name'),
                field('AI Model / System Name *', 'model_name'),
                field('Date of Filing', 'date', 'date'),
                field('Contact Name', 'contact_name'),
                field('Contact Email', 'contact_email', 'email'),
                field('Audit ID (optional)', 'audit_id'),
            ),
            React.createElement('button', {
                className: 'btn-primary',
                onClick: handleGenerate,
                disabled: generating,
            }, generating ? 'Generating...' : '📄 Generate Disclosure PDF'),
        ),
        React.createElement('div', { className: 'card' },
            React.createElement('h3', null, 'About This Form'),
            React.createElement('p', null, 'This generates a Federal Disclosure Form pursuant to the Comprehensive Licensing and Ethical AI Regulation (CLEAR) Act of 2026.'),
            React.createElement('p', null, 'If you provide an Audit ID from a previous copyright audit, the PDF will include detailed source-level risk analysis.'),
        ),
    );
}
window.DisclosureForm = DisclosureForm;
