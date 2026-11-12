#include "rule_engine.h"

std::vector<std::string> RuleEngine::filter(const std::vector<ArticleText>& articles, const Rule& rule) const {
    std::vector<std::string> matched;
    for (const auto& article : articles) {
        if (rule.matches(article)) {
            matched.push_back(article.id);
        }
    }
    return matched;
}
