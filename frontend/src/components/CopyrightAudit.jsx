function CopyrightAudit() {
    const [audit, setAudit] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [filter, setFilter] = React.useState('all');

    const handleFile = async (file) => {
        setLoading(true);
        try {
            const result = await api.runAudit(file);
            setAudit(result);
        } catch (e) {
            alert('Error running audit: ' + e.message);
        }
        setLoading(false);
    };

    const filteredRows = audit ? audit.rows.filter(r => filter === 'all' || r.risk_level === filter) : [];

    return React.createElement('div', { className: 'copyright-audit' },
        React.createElement('h2', null, 'Copyright Compliance Audit'),
        React.createElement('p', { className: 'subtitle' }, 'Upload a dataset manifest CSV to scan for copyright risk.'),
        React.createElement(FileUpload, { onFile: handleFile, accept: '.csv', label: 'Drop your manifest CSV here or click to browse' }),
        loading && React.createElement('div', { className: 'loading' }, 'Analyzing manifest...'),
        audit && React.createElement('div', null,
            React.createElement('div', { className: 'cards-grid' },
                React.createElement('div', { className: 'stat-card danger' },
                    React.createElement('div', { className: 'stat-value' }, audit.summary.high_risk_count),
                    React.createElement('div', { className: 'stat-label' }, 'High Risk'),
                ),
                React.createElement('div', { className: 'stat-card warning' },
                    React.createElement('div', { className: 'stat-value' }, audit.summary.medium_risk_count),
                    React.createElement('div', { className: 'stat-label' }, 'Medium Risk'),
                ),
                React.createElement('div', { className: 'stat-card success' },
                    React.createElement('div', { className: 'stat-value' }, audit.summary.low_risk_count),
                    React.createElement('div', { className: 'stat-label' }, 'Low Risk'),
                ),
                React.createElement('div', { className: 'stat-card' },
                    React.createElement('div', { className: 'stat-value' }, audit.summary.total_sources),
                    React.createElement('div', { className: 'stat-label' }, 'Total Sources'),
                ),
            ),
            React.createElement('div', { className: 'filter-bar' },
                ['all', 'high', 'medium', 'low', 'unknown'].map(f =>
                    React.createElement('button', {
                        key: f,
                        className: 'filter-btn' + (filter === f ? ' active' : ''),
                        onClick: () => setFilter(f),
                    }, f.charAt(0).toUpperCase() + f.slice(1))
                )
            ),
            React.createElement('table', { className: 'results-table' },
                React.createElement('thead', null,
                    React.createElement('tr', null,
                        React.createElement('th', null, 'Domain'),
                        React.createElement('th', null, 'Type'),
                        React.createElement('th', null, 'Words'),
                        React.createElement('th', null, 'Risk'),
                        React.createElement('th', null, 'Reason'),
                    )
                ),
                React.createElement('tbody', null,
                    ...filteredRows.map((row, i) =>
                        React.createElement('tr', { key: i },
                            React.createElement('td', null, row.domain),
                            React.createElement('td', null, row.content_type),
                            React.createElement('td', { className: 'num' }, formatters.number(row.word_count)),
                            React.createElement('td', null, React.createElement(RiskBadge, { level: row.risk_level })),
                            React.createElement('td', { className: 'reason' }, row.risk_reason),
                        )
                    )
                )
            ),
            React.createElement('div', { className: 'card recommendations' },
                React.createElement('h3', null, 'Recommendations'),
                ...audit.summary.recommendations.map((r, i) =>
                    React.createElement('p', { key: i }, r)
                )
            ),
            React.createElement('p', { className: 'audit-id' }, 'Audit ID: ' + audit.audit_id),
        ),
    );
}
window.CopyrightAudit = CopyrightAudit;
