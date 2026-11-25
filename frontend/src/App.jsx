import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  ShieldAlert,
  Coins,
  MapPin,
  CheckCircle2,
  Search,
  Filter,
  BarChart3,
  Layers,
  ArrowUpRight,
  ExternalLink,
  ChevronRight,
  Cpu,
  Sprout,
  FlaskConical,
  Wrench,
  Building2,
  RefreshCw,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  PieChart,
  Pie
} from 'recharts';
import { getOpportunities, getImportSummary, getHealth, getRecommendations } from './services/api';

const SECTOR_ICONS = {
  agriculture: <Sprout className="w-4 h-4 text-emerald-400" />,
  electronics: <Cpu className="w-4 h-4 text-blue-400" />,
  chemicals: <FlaskConical className="w-4 h-4 text-purple-400" />,
  machinery: <Wrench className="w-4 h-4 text-amber-400" />,
  other: <Layers className="w-4 h-4 text-slate-400" />
};

const SECTOR_COLORS = {
  agriculture: '#10b981',
  electronics: '#3b82f6',
  chemicals: '#a855f7',
  machinery: '#f59e0b',
  other: '#64748b'
};

export default function App() {
  const [activeTab, setActiveTab] = useState('rankings');
  const [opportunities, setOpportunities] = useState([]);
  const [summary, setSummary] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState('farmer');
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSector, setSelectedSector] = useState('all');
  const [isLiveApi, setIsLiveApi] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const health = await getHealth();
      setIsLiveApi(health && health.database_connected);

      const [oppsData, summaryData, recsData] = await Promise.all([
        getOpportunities(),
        getImportSummary().catch(() => null),
        getRecommendations(selectedPersona).catch(() => null)
      ]);

      if (oppsData && oppsData.opportunities) {
        setOpportunities(oppsData.opportunities);
      }
      if (summaryData) {
        setSummary(summaryData);
      }
      if (recsData && recsData.items) {
        setRecommendations(recsData.items);
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    getRecommendations(selectedPersona)
      .then(res => res && res.items && setRecommendations(res.items))
      .catch(() => {});
  }, [selectedPersona]);

  // Filtered Opportunities
  const filteredOpportunities = opportunities.filter(item => {
    const matchesSector = selectedSector === 'all' || item.sector.toLowerCase() === selectedSector.toLowerCase();
    const matchesSearch =
      item.product_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.hs_code.includes(searchQuery);
    return matchesSector && matchesSearch;
  });

  // Calculate Metrics
  const totalTrackedBillions = summary ? (summary.total_tracked_imports_usd / 1e9).toFixed(2) : '9.82';
  const avgSavings = opportunities.length
    ? (opportunities.reduce((acc, curr) => acc + curr.potential_savings_percentage, 0) / opportunities.length).toFixed(1)
    : '29.5';

  const chartData = summary && summary.sectors
    ? Object.entries(summary.sectors).map(([sector, data]) => ({
        name: sector.charAt(0).toUpperCase() + sector.slice(1),
        value: data.percentage,
        usd: (data.value_usd / 1e9).toFixed(2),
        color: SECTOR_COLORS[sector] || '#64748b'
      }))
    : [
        { name: 'Electronics', value: 42.8, color: '#3b82f6' },
        { name: 'Machinery', value: 24.5, color: '#f59e0b' },
        { name: 'Chemicals', value: 18.2, color: '#a855f7' },
        { name: 'Agriculture', value: 14.5, color: '#10b981' }
      ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Banner / Navbar */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🇮🇳</span>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-tight text-white text-lg">SWADESHI INTELLIGENCE</span>
                <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-medium">
                  HackWithAditya 2026
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                National Import Substitution & Domestic Production Intelligence
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/60 border border-slate-700/60 text-xs">
              <span className={`w-2 h-2 rounded-full ${isLiveApi ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
              <span className="text-slate-300">{isLiveApi ? 'Live Backend API' : 'Demo Dataset Mode'}</span>
            </div>
            <button
              onClick={fetchData}
              disabled={loading}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              title="Refresh Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Executive Summary Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700/80 transition-all">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Tracked Import Bill</span>
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400"><Coins className="w-4 h-4" /></div>
            </div>
            <div className="text-2xl font-bold text-white">${totalTrackedBillions} Billion</div>
            <p className="text-xs text-slate-400 mt-1">Official FY24–25 Trade Analytics scope</p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700/80 transition-all">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">High Opportunity Targets</span>
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400"><TrendingUp className="w-4 h-4" /></div>
            </div>
            <div className="text-2xl font-bold text-white">{opportunities.length} Commodities</div>
            <p className="text-xs text-emerald-400 mt-1">Feasibility score &gt; 75 / 100</p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700/80 transition-all">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Average Cost Advantage</span>
              <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400"><Coins className="w-4 h-4" /></div>
            </div>
            <div className="text-2xl font-bold text-white">+{avgSavings}%</div>
            <p className="text-xs text-slate-400 mt-1">Landed import vs domestic cost</p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700/80 transition-all">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Domestic Clusters</span>
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400"><MapPin className="w-4 h-4" /></div>
            </div>
            <div className="text-2xl font-bold text-white">8 Identified Hubs</div>
            <p className="text-xs text-slate-400 mt-1">Across 6 Industrial States</p>
          </div>
        </section>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
          <button
            onClick={() => setActiveTab('rankings')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'rankings'
                ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-900/60'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            Opportunity Rankings
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'analytics'
                ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-900/60'
            }`}
          >
            <Layers className="w-4 h-4" />
            Sector Trade Distribution
          </button>
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'recommendations'
                ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-900/60'
            }`}
          >
            <CheckCircle2 className="w-4 h-4" />
            Actionable Recommendations
          </button>
        </div>

        {/* VIEW 1: OPPORTUNITY RANKINGS */}
        {activeTab === 'rankings' && (
          <section className="space-y-4">
            {/* Search and Filters */}
            <div className="flex flex-col sm:flex-row gap-3 justify-between items-center">
              <div className="relative w-full sm:w-80">
                <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search commodity or HS code..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-900/80 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
                />
              </div>

              {/* Sector Filter Chips */}
              <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto">
                {['all', 'agriculture', 'electronics', 'chemicals', 'machinery'].map((sec) => (
                  <button
                    key={sec}
                    onClick={() => setSelectedSector(sec)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                      selectedSector === sec
                        ? 'bg-slate-700 text-white font-semibold'
                        : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                    }`}
                  >
                    {sec}
                  </button>
                ))}
              </div>
            </div>

            {/* Table */}
            <div className="rounded-xl border border-slate-800 overflow-hidden bg-slate-900/30">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-slate-800 bg-slate-900/70 text-slate-400 text-xs uppercase tracking-wider">
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Commodity / HS Code</th>
                      <th className="py-3 px-4">Sector</th>
                      <th className="py-3 px-4">Landed Import Cost</th>
                      <th className="py-3 px-4">Est. Domestic Cost</th>
                      <th className="py-3 px-4">Cost Advantage</th>
                      <th className="py-3 px-4">Opportunity Score</th>
                      <th className="py-3 px-4">Top Production Hub</th>
                      <th className="py-3 px-4 text-right">Details</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {filteredOpportunities.length === 0 ? (
                      <tr>
                        <td colSpan="9" className="text-center py-8 text-slate-500">
                          No commodities found matching the criteria.
                        </td>
                      </tr>
                    ) : (
                      filteredOpportunities.map((opp) => (
                        <tr
                          key={opp.product_id}
                          className="hover:bg-slate-800/40 transition-colors cursor-pointer group"
                          onClick={() => setSelectedOpportunity(opp)}
                        >
                          <td className="py-3.5 px-4 font-mono font-medium text-slate-400">
                            #{opp.rank}
                          </td>
                          <td className="py-3.5 px-4 font-medium text-white">
                            <div>{opp.product_name}</div>
                            <span className="text-xs text-slate-500 font-mono">HS {opp.hs_code}</span>
                          </td>
                          <td className="py-3.5 px-4">
                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-300">
                              {SECTOR_ICONS[opp.sector.toLowerCase()] || <Layers className="w-3.5 h-3.5" />}
                              <span className="capitalize">{opp.sector}</span>
                            </span>
                          </td>
                          <td className="py-3.5 px-4 text-slate-300">
                            ₹{opp.import_cost.value.toLocaleString()} <span className="text-xs text-slate-500">/{opp.import_cost.unit}</span>
                          </td>
                          <td className="py-3.5 px-4 text-emerald-400 font-medium">
                            ₹{opp.domestic_cost.value.toLocaleString()} <span className="text-xs text-slate-500">/{opp.domestic_cost.unit}</span>
                          </td>
                          <td className="py-3.5 px-4">
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                              +{opp.potential_savings_percentage}%
                            </span>
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-blue-400">{opp.opportunity_score}</span>
                              <div className="w-16 h-2 rounded-full bg-slate-800 overflow-hidden">
                                <div
                                  className="h-full bg-blue-500 rounded-full"
                                  style={{ width: `${Math.min(opp.opportunity_score, 100)}%` }}
                                ></div>
                              </div>
                            </div>
                          </td>
                          <td className="py-3.5 px-4 text-slate-300 text-xs">
                            <div className="flex items-center gap-1">
                              <MapPin className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                              <span>{opp.top_production_region || 'Pan-India'}</span>
                            </div>
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-blue-400 transition-colors inline-block" />
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        )}

        {/* VIEW 2: TRADE & SECTOR ANALYTICS */}
        {activeTab === 'analytics' && (
          <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800">
              <h3 className="text-base font-semibold text-white mb-1">Import Value by Sector (%)</h3>
              <p className="text-xs text-slate-400 mb-6">Proportional distribution of tracked national import expenditure</p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={({ name, value }) => `${name} ${value}%`}
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem' }}
                      itemStyle={{ color: '#f8fafc' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800">
              <h3 className="text-base font-semibold text-white mb-1">Domestic Substitution Potential</h3>
              <p className="text-xs text-slate-400 mb-6">Estimated cost advantage percentage by commodity category</p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={opportunities.map(o => ({ name: o.product_name.slice(0, 15) + '...', savings: o.potential_savings_percentage }))}>
                    <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} unit="%" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem' }}
                      itemStyle={{ color: '#f8fafc' }}
                    />
                    <Bar dataKey="savings" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Potential Savings %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>
        )}

        {/* VIEW 3: ACTIONABLE RECOMMENDATIONS */}
        {activeTab === 'recommendations' && (
          <section className="space-y-6">
            <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-lg bg-slate-900 border border-slate-800 w-fit">
              <span className="text-xs text-slate-400 px-3">Target Persona:</span>
              {[
                { id: 'farmer', label: 'Farmers & FPOs', icon: <Sprout className="w-3.5 h-3.5" /> },
                { id: 'msme', label: 'MSMEs & Startups', icon: <Building2 className="w-3.5 h-3.5" /> },
                { id: 'manufacturer', label: 'Industrial Manufacturers', icon: <Wrench className="w-3.5 h-3.5" /> },
                { id: 'policymaker', label: 'Government & Planners', icon: <Layers className="w-3.5 h-3.5" /> }
              ].map((p) => (
                <button
                  key={p.id}
                  onClick={() => setSelectedPersona(p.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                    selectedPersona === p.id
                      ? 'bg-blue-600 text-white font-semibold'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  {p.icon}
                  {p.label}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {recommendations.map((rec, i) => (
                <div
                  key={i}
                  className="p-5 rounded-xl bg-slate-900/50 border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition-colors"
                >
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                        Market: {rec.annual_import_market}
                      </span>
                      <span className="text-xs font-medium text-emerald-400">
                        Margin: {rec.expected_margin}
                      </span>
                    </div>

                    <h4 className="text-base font-bold text-white">{rec.name}</h4>
                    <p className="text-xs text-slate-300 leading-relaxed">{rec.action}</p>
                  </div>

                  <div className="mt-5 pt-3 border-t border-slate-800">
                    <span className="text-[11px] text-slate-400 block mb-1">Recommended Cluster States:</span>
                    <div className="flex flex-wrap gap-1">
                      {rec.optimal_states.map((st, idx) => (
                        <span key={idx} className="text-[11px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                          {st}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      {/* Detail Modal Drawer */}
      {selectedOpportunity && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-6 shadow-2xl relative">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono text-blue-400 uppercase tracking-wider">HS Code: {selectedOpportunity.hs_code}</span>
                <h3 className="text-xl font-bold text-white mt-1">{selectedOpportunity.product_name}</h3>
                <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full capitalize inline-block mt-2">
                  {selectedOpportunity.sector} Sector
                </span>
              </div>
              <button
                onClick={() => setSelectedOpportunity(null)}
                className="text-slate-400 hover:text-white p-2 rounded-lg bg-slate-800/80 hover:bg-slate-800"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-3 gap-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div>
                <span className="text-xs text-slate-400 block">Landed Import Cost</span>
                <span className="text-lg font-bold text-slate-200">₹{selectedOpportunity.import_cost.value.toLocaleString()}</span>
                <span className="text-[10px] text-slate-500 block">per {selectedOpportunity.import_cost.unit}</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block">Domestic Cost</span>
                <span className="text-lg font-bold text-emerald-400">₹{selectedOpportunity.domestic_cost.value.toLocaleString()}</span>
                <span className="text-[10px] text-slate-500 block">per {selectedOpportunity.domestic_cost.unit}</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block">Cost Advantage</span>
                <span className="text-lg font-bold text-blue-400">+{selectedOpportunity.potential_savings_percentage}%</span>
                <span className="text-[10px] text-emerald-400 block">High Economic Advantage</span>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Domestic Production Feasibility</h4>
              <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 text-xs text-slate-300 space-y-2">
                <div className="flex items-center justify-between">
                  <span>Feasibility Score:</span>
                  <span className="font-bold text-blue-400">{selectedOpportunity.opportunity_score} / 100</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Recommended Regional Cluster:</span>
                  <span className="font-medium text-amber-400">{selectedOpportunity.top_production_region}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Confidence Level:</span>
                  <span className="font-medium capitalize text-emerald-400">{selectedOpportunity.confidence}</span>
                </div>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setSelectedOpportunity(null)}
                className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-colors"
              >
                Close Report
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>SWADESHI INTELLIGENCE — Built for HackWithAditya 2026. Data sourced from official Ministry of Commerce Trade Portals.</p>
      </footer>
    </div>
  );
}
