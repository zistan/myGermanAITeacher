/**
 * ProgressChart Component
 * Multi-purpose recharts wrapper for line, bar, and area charts
 */

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

export interface ProgressChartProps {
  data: any[];
  type: 'line' | 'bar' | 'area';
  xAxisKey: string;
  yAxisKey: string;
  color?: string;
  height?: number;
  showLegend?: boolean;
  yAxisLabel?: string;
}

export function ProgressChart({
  data,
  type,
  xAxisKey,
  yAxisKey,
  color = '#3b82f6',
  height = 300,
  showLegend = false,
  yAxisLabel,
}: ProgressChartProps) {
  // Select chart type
  const ChartComponent = type === 'line' ? LineChart : type === 'bar' ? BarChart : AreaChart;

  return (
    <ResponsiveContainer width="100%" height={height}>
      <ChartComponent data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis
          dataKey={xAxisKey}
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
        />
        <YAxis
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
          label={
            yAxisLabel
              ? {
                  value: yAxisLabel,
                  angle: -90,
                  position: 'insideLeft',
                  style: { fontSize: '12px', fill: '#6b7280' },
                }
              : undefined
          }
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#fff',
            border: '1px solid #e5e7eb',
            borderRadius: '6px',
            fontSize: '12px',
          }}
        />
        {showLegend && <Legend />}
        {type === 'line' && (
          <Line
            type="monotone"
            dataKey={yAxisKey}
            stroke={color}
            strokeWidth={2}
            dot={{ fill: color, r: 4 }}
            activeDot={{ r: 6 }}
          />
        )}
        {type === 'bar' && (
          <Bar
            dataKey={yAxisKey}
            fill={color}
            radius={[4, 4, 0, 0]}
          />
        )}
        {type === 'area' && (
          <Area
            type="monotone"
            dataKey={yAxisKey}
            stroke={color}
            fill={color}
            fillOpacity={0.3}
          />
        )}
      </ChartComponent>
    </ResponsiveContainer>
  );
}
