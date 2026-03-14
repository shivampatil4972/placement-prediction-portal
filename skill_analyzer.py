"""
Skill Gap Analysis Utility
Analyzes student skills and provides recommendations
"""

import re

from config import Config

class SkillGapAnalyzer:
    """Analyze skill gaps and provide recommendations"""

    SKILL_ALIASES = {
        'js': 'javascript',
        'javascript': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'python3': 'python',
        'nodejs': 'node.js',
        'node js': 'node.js',
        'reactjs': 'react',
        'react js': 'react',
        'ml': 'machine learning',
        'dsa': 'data structures and algorithms',
        'data structures': 'data structures and algorithms',
        'algorithms': 'data structures and algorithms',
        'git hub': 'github',
        'restful api': 'rest api'
    }

    DISPLAY_NAMES = {
        'sql': 'SQL',
        'api': 'API',
        'ai': 'AI',
        'nlp': 'NLP',
        'oop': 'OOP',
        'c++': 'C++',
        'c#': 'C#',
        'aws': 'AWS',
        'html': 'HTML',
        'css': 'CSS',
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'python': 'Python',
        'github': 'GitHub',
        'git': 'Git',
        'rest api': 'REST API',
        'machine learning': 'Machine Learning',
        'data structures and algorithms': 'Data Structures and Algorithms'
    }

    @staticmethod
    def _normalize_skill(skill):
        cleaned = re.sub(r'\s+', ' ', str(skill).strip().lower())
        if not cleaned:
            return ''
        return SkillGapAnalyzer.SKILL_ALIASES.get(cleaned, cleaned)

    @staticmethod
    def _display_skill(normalized_skill):
        if normalized_skill in SkillGapAnalyzer.DISPLAY_NAMES:
            return SkillGapAnalyzer.DISPLAY_NAMES[normalized_skill]
        return normalized_skill.title()

    @staticmethod
    def _parse_skills(skills_text):
        if not skills_text:
            return []
        parts = re.split(r'[,\n;]+', str(skills_text))
        parsed = []
        seen = set()
        for part in parts:
            normalized = SkillGapAnalyzer._normalize_skill(part)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            parsed.append(normalized)
        return parsed

    @staticmethod
    def _build_action(action, impact_score, rationale):
        if impact_score >= 8:
            impact_label = 'High'
        elif impact_score >= 5:
            impact_label = 'Medium'
        else:
            impact_label = 'Low'
        return {
            'action': action,
            'impact_score': impact_score,
            'impact_label': impact_label,
            'rationale': rationale
        }
    
    @staticmethod
    def analyze(profile_data, placement_probability):
        """
        Perform comprehensive skill gap analysis
        
        Args:
            profile_data: Student profile dictionary
            placement_probability: Current placement probability
        
        Returns:
            Dictionary with analysis results
        """
        
        branch = profile_data.get('branch', '')
        current_skills = profile_data.get('skills', '')
        cgpa = profile_data.get('cgpa', 0)
        internship_count = profile_data.get('internship_count', 0)
        project_count = profile_data.get('project_count', 0)
        certification_count = profile_data.get('certification_count', 0)
        
        current_skills_list = SkillGapAnalyzer._parse_skills(current_skills)
        
        # Get important skills for branch
        important_skills = Config.BRANCH_IMPORTANT_SKILLS.get(
            branch,
            Config.BRANCH_IMPORTANT_SKILLS['Computer Science']
        )
        important_skills_norm = [SkillGapAnalyzer._normalize_skill(skill) for skill in important_skills]
        
        # Find missing skills
        missing_skills_norm = [skill for skill in important_skills_norm if skill and skill not in current_skills_list]
        missing_skills = [SkillGapAnalyzer._display_skill(skill) for skill in missing_skills_norm]
        matched_important_skills = [
            skill for skill in important_skills_norm if skill and skill in current_skills_list
        ]

        strengths = []
        if cgpa >= 8.5:
            strengths.append('Strong academic consistency (CGPA 8.5+)')
        if internship_count >= 2:
            strengths.append('Good internship exposure')
        if project_count >= 3:
            strengths.append('Strong project portfolio')
        if certification_count >= 2:
            strengths.append('Certification-backed profile')
        if len(current_skills_list) >= 8:
            strengths.append('Broad technical skill coverage')
        
        # Weighted gap scoring for consistent priority decisions.
        skill_gap_ratio = (len(missing_skills_norm) / len(important_skills_norm)) if important_skills_norm else 0
        cgpa_gap_ratio = max(0.0, (8.0 - float(cgpa)) / 3.0)
        internship_gap_ratio = max(0.0, (2 - int(internship_count)) / 2.0)
        project_gap_ratio = max(0.0, (3 - int(project_count)) / 3.0)
        cert_gap_ratio = max(0.0, (1 - int(certification_count)) / 1.0)
        probability_gap_ratio = max(0.0, (70 - float(placement_probability)) / 70.0)

        overall_gap = (
            0.35 * skill_gap_ratio +
            0.20 * internship_gap_ratio +
            0.15 * project_gap_ratio +
            0.15 * cgpa_gap_ratio +
            0.05 * cert_gap_ratio +
            0.10 * probability_gap_ratio
        )
        readiness_score = round(max(0.0, min(100.0, (1 - overall_gap) * 100)), 1)

        if readiness_score < 50:
            priority = 'High'
        elif readiness_score < 75:
            priority = 'Medium'
        else:
            priority = 'Low'

        action_pool = []

        if placement_probability < 40:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Focus this week on internship applications and one deployable project to improve short-term placement readiness.',
                10,
                'Low current probability requires immediate high-impact profile actions.'
            ))

        if cgpa < 7.0:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Improve CGPA above 7.0 using a focused weekly study plan.',
                8,
                'CGPA below baseline often filters students out in early screening.'
            ))
        elif cgpa < 8.0:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Target CGPA 8.0+ to unlock stronger company shortlists.',
                5,
                'Higher CGPA increases eligibility for premium roles.'
            ))

        if internship_count < 2:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Complete at least 1-2 internships with documented outcomes.',
                9,
                'Internship exposure is a strong placement signal in your model profile.'
            ))

        if project_count < 3:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Build 2-3 projects and publish clean documentation on GitHub.',
                8,
                'Project depth strongly improves interview conversion and technical fit.'
            ))

        if len(current_skills_list) < 6:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Expand your technical stack to at least 6-8 relevant skills.',
                7,
                'Broader skill coverage improves role matching and resume quality.'
            ))

        if missing_skills:
            action_pool.append(SkillGapAnalyzer._build_action(
                f'Prioritize these branch-critical skills: {", ".join(missing_skills[:3])}.',
                8,
                'Missing branch-critical skills reduce role alignment.'
            ))

        if 'data structures and algorithms' not in current_skills_list:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Practice Data Structures and Algorithms daily for technical rounds.',
                9,
                'DSA preparation is essential for coding interviews.'
            ))

        if 'git' not in current_skills_list and 'github' not in current_skills_list:
            action_pool.append(SkillGapAnalyzer._build_action(
                'Learn Git/GitHub workflows and showcase project commits publicly.',
                5,
                'Version-control visibility helps recruiters assess execution quality.'
            ))

        action_pool.append(SkillGapAnalyzer._build_action(
            'Schedule weekly mock interviews for communication and aptitude readiness.',
            6,
            'Interview readiness often determines final conversion despite strong profiles.'
        ))

        action_pool = sorted(action_pool, key=lambda x: x['impact_score'], reverse=True)
        top_actions = action_pool[:3]

        recommendations = []
        if readiness_score < 50:
            recommendations.append('⚠️ Your readiness is currently low. Address the top actions immediately for the highest uplift.')
        elif readiness_score < 75:
            recommendations.append('Your readiness is moderate. Consistent improvements can move you into a strong placement zone.')
        else:
            recommendations.append('✅ Strong profile overall. Focus on interview performance and advanced role preparation.')

        for action in top_actions:
            recommendations.append(f"[{action['impact_label']} Impact] {action['action']}")

        if placement_probability >= 70 and cgpa >= 8.0:
            recommendations.append('You are competitive for top-tier companies. Prepare system design and advanced problem-solving now.')

        confidence = 'High' if len(current_skills_list) >= 6 else 'Medium'
        
        return {
            'missing_skills': missing_skills,
            'missing_skills_str': ', '.join(missing_skills) if missing_skills else 'None',
            'recommendations': recommendations,
            'priority': priority,
            'skill_coverage': (
                round(
                    max(0.0, min(100.0, (len(matched_important_skills) / len(important_skills_norm)) * 100)),
                    1
                )
                if important_skills_norm else 100
            ),
            'readiness_score': readiness_score,
            'top_actions': top_actions,
            'strengths': strengths,
            'confidence': confidence,
            'normalized_skills': [SkillGapAnalyzer._display_skill(skill) for skill in current_skills_list]
        }
    
    @staticmethod
    def get_improvement_areas(profile_data):
        """Get quick list of improvement areas"""
        areas = []
        
        if profile_data.get('cgpa', 0) < 7.0:
            areas.append('CGPA')
        
        if profile_data.get('internship_count', 0) < 2:
            areas.append('Internships')
        
        if profile_data.get('project_count', 0) < 2:
            areas.append('Projects')
        
        skills = SkillGapAnalyzer._parse_skills(profile_data.get('skills', ''))
        skill_count = len(skills)
        
        if skill_count < 5:
            areas.append('Technical Skills')
        
        if profile_data.get('certification_count', 0) == 0:
            areas.append('Certifications')
        
        return areas
    
    @staticmethod
    def suggest_skills_to_learn(branch, current_skills_list):
        """Suggest top 3 skills to learn based on branch"""
        important_skills = Config.BRANCH_IMPORTANT_SKILLS.get(
            branch,
            Config.BRANCH_IMPORTANT_SKILLS['Computer Science']
        )
        important_norm = [SkillGapAnalyzer._normalize_skill(skill) for skill in important_skills]

        current_norm = set()
        for skill in current_skills_list:
            normalized = SkillGapAnalyzer._normalize_skill(skill)
            if normalized:
                current_norm.add(normalized)

        missing = [skill for skill in important_norm if skill and skill not in current_norm]
        display_missing = [SkillGapAnalyzer._display_skill(skill) for skill in missing]

        return display_missing[:3] if display_missing else []


# Convenience instance
skill_analyzer = SkillGapAnalyzer()
