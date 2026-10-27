// Official verification is pending; see docs/sources.md. No official subject quotas asserted.
export const QUALIFICATION = {
 name: "미용사(네일)", subjects: ["네일미용 통합"] as const,
 questionCount: 60, durationMinutes: 60, choiceCount: 4, passScore: 60,
 rulesVerificationStatus: "pending", selectionPolicy: "통합 무작위 학습용 추출",
 hasSubjectCutoff: false, areas: ["네일 개론", "피부·손발톱", "위생·안전", "화장품·재료", "네일 기술"],
} as const;
