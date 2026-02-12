function RiskBadge({ level }) {
    const color = formatters.riskColor(level);
    return React.createElement('span', {
        className: 'risk-badge',
        style: { backgroundColor: color + '22', color: color, borderColor: color },
    }, level.toUpperCase());
}
window.RiskBadge = RiskBadge;
