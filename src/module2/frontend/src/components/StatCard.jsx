export default function StatCard({ title, value, icon: Icon, trend }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between min-w-0">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-slate-500 truncate">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-slate-800">{value}</p>
        </div>
        {Icon && (
          <div className="w-12 h-12 rounded-full bg-teal-50 flex items-center justify-center text-teal-600 shrink-0">
            <Icon size={24} />
          </div>
        )}
      </div>
      {trend && (
        <div className="mt-4 flex items-center text-sm">
          <span className={trend.isPositive ? 'text-teal-600' : 'text-red-500'}>
            {trend.isPositive ? '↑' : '↓'} {trend.value}
          </span>
          <span className="ml-2 text-slate-500 truncate">vs last month</span>
        </div>
      )}
    </div>
  );
}
