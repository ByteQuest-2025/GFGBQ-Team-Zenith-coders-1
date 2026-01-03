export const mockComplaints = [
  {
    id: '1',
    complaint_id: 'COMP-2026-001234',
    title: 'Broken streetlight on Main Road',
    description: 'The streetlight has been non-functional for 3 days causing safety issues',
    category: 'Utilities',
    category_confidence: 0.91,
    urgency_level: 'HIGH',
    urgency_score: 0.85,
    status: 'ASSIGNED',
    assigned_department: 'Electricity Board',
    assigned_officer: { name: 'Officer Kumar' },
    location: { address: 'Main Road, Sriperumbudur', latitude: 12.9716, longitude: 77.5946 },
    attachments: [],
    status_history: [
      { status: 'SUBMITTED', timestamp: '2026-01-01T10:00:00Z', notes: 'Complaint received' },
      { status: 'TRIAGED', timestamp: '2026-01-01T10:15:00Z', notes: 'AI classified as high urgency' },
      { status: 'ASSIGNED', timestamp: '2026-01-01T11:00:00Z', notes: 'Assigned to Electricity Board' }
    ],
    created_at: '2026-01-01T10:00:00Z'
  },
  {
    id: '2',
    complaint_id: 'COMP-2026-001235',
    title: 'Pothole on Highway',
    description: 'Large pothole causing accidents',
    category: 'Roads',
    category_confidence: 0.95,
    urgency_level: 'MEDIUM',
    urgency_score: 0.62,
    status: 'IN_PROGRESS',
    assigned_department: 'PWD',
    assigned_officer: { name: 'Officer Sharma' },
    location: { address: 'NH-48, Sriperumbudur', latitude: 12.9716, longitude: 77.5946 },
    attachments: [],
    status_history: [
      { status: 'SUBMITTED', timestamp: '2026-01-02T09:00:00Z', notes: 'Complaint received' },
      { status: 'TRIAGED', timestamp: '2026-01-02T09:10:00Z', notes: 'AI classified as medium urgency' },
      { status: 'ASSIGNED', timestamp: '2026-01-02T10:00:00Z', notes: 'Assigned to PWD' },
      { status: 'IN_PROGRESS', timestamp: '2026-01-03T08:00:00Z', notes: 'Repair work started' }
    ],
    created_at: '2026-01-02T09:00:00Z'
  },
  {
    id: '3',
    complaint_id: 'COMP-2026-001236',
    title: 'Water supply disruption',
    description: 'No water supply in the area for the past 2 days',
    category: 'Water',
    category_confidence: 0.88,
    urgency_level: 'HIGH',
    urgency_score: 0.78,
    status: 'RESOLVED',
    assigned_department: 'Water Board',
    assigned_officer: { name: 'Officer Patel' },
    location: { address: 'Gandhi Nagar, Sriperumbudur', latitude: 12.9716, longitude: 77.5946 },
    attachments: [],
    status_history: [
      { status: 'SUBMITTED', timestamp: '2025-12-30T08:00:00Z', notes: 'Complaint received' },
      { status: 'TRIAGED', timestamp: '2025-12-30T08:10:00Z', notes: 'AI classified as high urgency' },
      { status: 'ASSIGNED', timestamp: '2025-12-30T09:00:00Z', notes: 'Assigned to Water Board' },
      { status: 'IN_PROGRESS', timestamp: '2025-12-30T14:00:00Z', notes: 'Repair team dispatched' },
      { status: 'RESOLVED', timestamp: '2025-12-31T10:00:00Z', notes: 'Water supply restored' }
    ],
    created_at: '2025-12-30T08:00:00Z'
  }
];