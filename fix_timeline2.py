with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("export const WeeklyTimeline: React.FC<WeeklyTimelineProps> = ({\n  const navigate = useNavigate();", "export const WeeklyTimeline: React.FC<WeeklyTimelineProps> = ({\n  milestones,\n  onCompleteCourse,\n}) => {\n  const navigate = useNavigate();")

with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
