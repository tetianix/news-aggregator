#pragma once

#include <string>
#include <vector>

#include "rule.h"

class RuleEngine {
public:
    std::vector<std::string> filter(const std::vector<ArticleText>& articles, const Rule& rule) const;
};
