// ==============================================================================
// AI KARMAYOGI — RADAR CHART COMPONENT
// Recharts Visualization Comparing Mandated vs Demonstrated FRAC Proficiency
// ==============================================================================

import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { CompetencyDeficitItem } from '@/types';
import { Compass } from 'lucide-react';

interface RadarChartCardProps {
  competencies: CompetencyDeficitItem[];
}

export const RadarChartCard: React.FC<RadarChartCardProps> = ({ competencies }) => {
  const chartData = competencies.map((comp) => {
    // Truncate long names for radar axis readability
    const shortName = comp.competency_name.length > 22
      ? `${comp.competency_name.substring(0, 20)}...`
      : comp.competency_name;

    return {
      subject: shortName,
      fullName: comp.competency_name,
      mandated: comp.mandated_level,
      demonstrated: comp.demonstrated_level,
      code: comp.competency_code,
      type: comp.competency_type,
    };
  });

  return (
    <Card className="border-slate-200  shadow-sm">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <CardTitle className="text-base flex items-center gap-2">
              <Compass className="h-4 w-4 text-teal-600" />
              FRAC Competency Radar Profile
            </CardTitle>
            <CardDescription className="text-xs">
              Direct comparison between role-mandated baseline and evaluated capability.
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-2">
        <div className="h-[340px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={chartData} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
              <PolarGrid stroke="#94a3b8" strokeOpacity={0.3} />
              <PolarAngleAxis
                dataKey="subject"
                tick={{ fill: '#64748b', fontSize: 11, fontWeight: 500 }}
              />
              <PolarRadiusAxis
                angle={90}
                domain={[0, 5]}
                tickCount={6}
                tick={{ fill: '#94a3b8', fontSize: 10 }}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="rounded-xl border border-slate-200  bg-white/95 /95 backdrop-blur-md p-3 shadow-xl text-xs space-y-1">
                        <p className="font-bold text-slate-900 ">{data.fullName}</p>
                        <p className="text-[10px] text-slate-600 uppercase tracking-wider">{data.code} • {data.type}</p>
                        <div className="pt-1.5 space-y-1 border-t border-slate-100 ">
                          <p className="text-teal-600  font-medium">
                            Mandated Level: <span className="font-bold">Level {data.mandated}</span>
                          </p>
                          <p className="text-teal-600  font-medium">
                            Demonstrated Level: <span className="font-bold">Level {data.demonstrated}</span>
                          </p>
                          <p className="text-slate-500 text-[10px]">
                            Gap: {Math.max(0, data.mandated - data.demonstrated)} Level(s)
                          </p>
                        </div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Radar
                name="Mandated Level"
                dataKey="mandated"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.15}
                strokeWidth={2}
              />
              <Radar
                name="Demonstrated Level"
                dataKey="demonstrated"
                stroke="#10b981"
                fill="#10b981"
                fillOpacity={0.35}
                strokeWidth={2}
              />
              <Legend
                wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
                iconType="circle"
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};
